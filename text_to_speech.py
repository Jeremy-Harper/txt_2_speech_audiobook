import os
import re
import sys
import tempfile
import glob
from google.cloud import texttospeech
from replacements import text_rules, math_rules

# Define break times in seconds
SECTION_BREAK = 2  # Adjust the time as needed
CAPTION_BREAK = 1  # Adjust the time as needed


# Define directories
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
SOURCE_DIR = os.getenv('SOURCE_DIR', PROJECT_DIR)  # Default to PROJECT_DIR if SOURCE_DIR not set
DELIVERY_DIR = os.path.join(PROJECT_DIR, "audiobook")

# Ensure DELIVERY_DIR exists
os.makedirs(DELIVERY_DIR, exist_ok=True)

# Set Google Cloud credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(PROJECT_DIR, "texttospeech.json")

# Initialize Text-to-Speech client
speech_client = texttospeech.TextToSpeechClient()

# Function definitions
def replace_nested(expr, rules):
    changed = True
    while changed:
        changed = False
        for pattern, replacement in rules:
            new_expr, replacements_made = re.subn(pattern, replacement, expr)
            if replacements_made > 0:
                changed = True
                expr = new_expr
    return expr

def process_ssml(ssml, rules):
    while re.search(r"\\\((.*?)\\\)", ssml):
        ssml = re.sub(r"\\\((.*?)\\\)", lambda match: replace_nested(match.group(1), rules), ssml)
    return ssml

def remove_urls(line: str) -> str:
    return re.sub("https?://[\w/:%#\$&\?\(\)~\.=\+\-]+", "", line)

def remove_references(line: str) -> str:
    line = re.sub(r'\s*\[[^\]]*, \d{4}(?:, [^\]]*, \d{4})*\]', '', line)
    line = re.sub(r'\s*\([^\)]*, \d{4}(?:[;,] [^\)]*, \d{4}[a-zA-Z]*?)*\)', '', line)
    return line

def remove_markdown_syntax(line: str) -> str:
    line = re.sub(r"\*\*(.*?)\*\*", r"\1", line)  # bold
    line = re.sub(r"_(.*?)_", r"\1", line)  # italic
    line = re.sub(r"^\* ", "", line)  # bullet points
    return line.replace('`', '')  # inline code

def apply_text_rules(line: str) -> str:
    for pattern, replacement in text_rules:
        line = re.sub(pattern, replacement, line)
    return line

def process_line(line: str) -> str:
    line = remove_urls(line)
    line = remove_references(line)
    line = remove_markdown_syntax(line)
    line = apply_text_rules(line)
    return line


class MP3Generator:
    def __init__(self, md_filename, output_dir, language_code, voice_name):
        self.md_filename = md_filename
        self.output_dir = output_dir
        self.language_code = language_code
        self.voice_name = voice_name
        self.ssml = ""
        self.mp3_file_list = []
        self.temp_path = tempfile.gettempdir()
        self.title_flag = True
        self.table_flag = False
    
    def generate_mp3_for_ssml(self, filename, ssml):
        print("Started generating speech for {}".format(filename))
        ssml = "<speak>\n" + ssml + "</speak>\n"
        synthesis_input = texttospeech.SynthesisInput(ssml=ssml)
        voice = texttospeech.VoiceSelectionParams(language_code=self.language_code, name=self.voice_name)
        audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
        try:
            response = speech_client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
        except Exception as e:
            print(f"Error generating speech for {filename}: {e}")
            # Handle the exception or try an alternative configuration as needed
            return None
        output_file_path = os.path.join(self.output_dir, filename)
        with open(output_file_path, "wb") as out:
            out.write(response.audio_content)
        print("MP3 file saved: {}".format(output_file_path))
        return output_file_path
        
    def handle_line(self, line):
        section_break = f'<break time="{SECTION_BREAK}s"/>'
        caption_break = f'<break time="{CAPTION_BREAK}s"/>'

        inline_footnote = re.match(r"^(.*)Footnote [0-9]+:.*", line)
        inline_header = re.match(r"\*\*(.*?)\*\*\s*([A-Z])", line)

        if re.match(r"^#{1,6} .*", line):
            line = re.sub(r"^#{1,6} ", "", line)
            self.ssml += f"{section_break}<p>{line}</p>{section_break}\n"
        elif inline_header:
            self.ssml += f"{section_break}<p>{inline_header.group(1)}</p>{section_break}\n"
            self.ssml += f"<p>{inline_header.group(2)}</p>\n"
        elif re.match(r"^\\begin{table}", line):
            self.table_flag = True
        elif re.match(r"^\\end{table}", line):
            self.table_flag = False
        elif self.table_flag:
            pass
        elif re.match(r"^Figure [0-9]+:", line) or re.match(r"^Table [0-9]+:", line):
            self.ssml += f"{caption_break}{line}{caption_break}\n"
        elif inline_footnote:
            self.ssml += f"{inline_footnote.group(1)}\n"
        elif re.match(r"^\\\[.*\\\]", line):
            self.ssml += section_break
        else:
            self.ssml += f"<p>{line}</p>\n"

    def generate_mp3_files(self):
        with open(self.md_filename, "r") as md_file:
            for id, line in enumerate(md_file.readlines()):
                line = process_line(line)

                if len(self.ssml.encode("utf-8")) + len(line.encode("utf-8")) > 4500:
                    filename = f'{os.path.basename(self.md_filename)[:-4]}-{id}.mp3'
                    # Corrected line below
                    mp3_file = self.generate_mp3_for_ssml(filename, self.ssml)
                    self.mp3_file_list.append(mp3_file)
                    self.ssml = ""

                if self.title_flag and id != 0:
                    if "# Abstract" in line or len(line) > 200:
                        self.title_flag = False
                    else:
                        continue

                self.handle_line(line)

                if re.search(r"\\\((.*)\\\)", self.ssml):
                    self.ssml = process_ssml(self.ssml, math_rules)

            if self.ssml:
                filename = f'{os.path.basename(self.md_filename)[:-4]}-{id}.mp3'
                # Corrected line below
                mp3_file = self.generate_mp3_for_ssml(filename, self.ssml)
                self.mp3_file_list.append(mp3_file)

        return self.mp3_file_list


def merge_mp3_files(out_path, mp3_file_list):

    # merge saved mp3 files
    print("Started merging mp3 files...")

    # save the merged mp3 file
    merged_mp3_file_name = (
        re.sub("-[0-9]+.mp3", ".mp3", os.path.basename(mp3_file_list[0]))
    )  # 'foo-101' -> 'foo.mp3'
    with open(os.path.join(out_path, merged_mp3_file_name), "wb") as out:
        for mp3_file in mp3_file_list:
            with open(mp3_file, "rb") as mp3:
                out.write(mp3.read())

    # delete mp3 files
    for mp3_file in mp3_file_list:
        os.remove(mp3_file)
    print("Ended merging mp3 files: {}".format(merged_mp3_file_name))

# Main execution
if __name__ == "__main__":
    for md_filename in glob.glob(os.path.join(SOURCE_DIR, "*.md")):
        mp3_generator = MP3Generator(md_filename)
        mp3_file_list = mp3_generator.generate_mp3_files()
