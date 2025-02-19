I copied from paper2speech and modified it so that I could take a txt file and have it be generated into an audiobook, I've used it to generate a 20hr+ audiobook. This uses a txt file directly.
# Markdown to Audiobook Converter

This Python project converts markdown files into audiobooks using Text-to-Speech (TTS) technology. It leverages Google Cloud's Text-to-Speech API to generate MP3 files from the text content of markdown files. This tool is perfect for creating audiobooks, podcasts, or any audio content from written documents.

## Features

- Support for multiple voice options
- Conversion of markdown syntax to plain text suitable for TTS
- Handling of special syntax in markdown for improved audio quality

## Prerequisites

Before you can use this tool, ensure you have the following:

- Python 3.x installed on your system
- A Google Cloud account with Text-to-Speech API enabled
- The google-cloud-texttospeech library installed
- A Google Cloud service account key file (texttospeech.json)

## Installation

1. Clone this repository to your local machine.

    ```sh
    git clone <repository-url>
    ```

2. Navigate into the project directory.

    ```sh
    cd <project-directory>
    ```

2.a I recommend creating a virtual machine
    ```sh
    python3 -m venv audiobook
    source audiobook/bin/activate
    ```

3. Install the required Python dependencies.

    ```sh
    pip install -r requirements.txt
    ```

## Configuration

- Place your Google Cloud service account key file (texttospeech.json) in the project directory.
- If you want to change the source directory for markdown files, set the SOURCE_DIR environment variable to the desired path.

## Usage

You'll need to create folders audio_book & text_files

To convert a markdown file into an MP3 audiobook, use the `main.py` script with the following syntax:

```sh
python main.py <path-to-markdown-file> -o <output-directory> -v <voice-option>
```

Parameters:

    <path-to-markdown-file>: The path to the markdown file you want to convert.
    <output-directory>: (Optional) The directory where the output MP3 files will be saved. Default is ./audiobook.
    <voice-option>: (Optional) The voice selection for the TTS conversion. Default is 1. Available voices are:
        1: English (US) Female (en-US-Wavenet-F)
        2: English (GB) Male (en-GB-Wavenet-B)
        Add more voice options as needed in the voices dictionary within main.py.

Adding More Voices

To add more voices, update the voices dictionary in main.py with the new voice's language code and name, following the structure of the existing entries.

### Example
Assuming you have your book file(s) in a directory named ./text_files and you want to save the generated audiobook MP3 files in a directory named ./audio_book, follow the example below:

```sh
python main.py ./text_files/my_book_file.txt -o ./audio_book -v 1
```

FYI - 
I created bulk_docx_to_txt.py to allow me to move all docx files in a folder into txt. I used this to generate voice files specific to chapters. (If you are using a word doc with proper headers you are able to use word's features to split apart by the header level into many docx files. *Note don't do this with your original file, create a copy)



# Paper2Speech (ORIGINAL INSTRUCTIONS)

## Motivation
As a student in applied mathematics / machine learning, I often get to read scientific books, lecture notes and papers.
Usually I prefer listening to a lecture from the professor and following his visual explanations on the blackboard, because then I get much information through the ear and don't have to do the "heavy lifting" through reading only.
So far, this has not been available for books and papers.  
So I thought: Why not let a software read out the text for you?
What if you just had to click a button in the Finder, and the book or paper is converted to speech automatically?  
This script uses the Meta [Nougat](https://facebookresearch.github.io/nougat/) package to extract formatted text from pdf and then converts it to audio using the [Google Cloud Text to Speech API](https://cloud.google.com/text-to-speech?hl=de).

Sample output for the paper [Large Language Models for Compiler Optimization](https://arxiv.org/abs/2309.07062):  
[output audio](https://github.com/kaieberl/paper2speech/blob/main/Large%20Language%20Models%20for%20Compiler%20Optimization.mp4)  
<img src="https://github.com/kaieberl/paper2speech/blob/main/Large%20Language%20Models%20for%20Compiler%20Optimization.jpg" width="500">

## Capabilities
- pause before and after headings
- skip references like \[1\], \(1, 2)], \[Feynman et al., 1965\], \[AAKA23, SKNM23\]
- spell out abbreviations like e.g., i.e., w.r.t., Fig., Eq.
- read out inline math (work in progress)
- do not read out block math, instead pause
- do not read out table contents
- read out figure, table captions

## Usage
```bash
pip3 install -r requirements.txt
```
```bash
python3 main.py <input_file> -o <output_path>
```

The Google cloud authentication json file should be in the same directory as the main.py file. It can be downloaded from the Google Cloud Console, as described [here](https://cloud.google.com/api-keys/docs/create-manage-api-keys).  
TLDR: On [https://cloud.google.com](https://cloud.google.com), create a new project. In your project, in the upper right corner, click on the 3 dots > project settings > service accounts > choose one or create service account > create key > json > create.
The resulting json file should be downloaded automatically.
Google TTS is free for the first 1 million characters per month, then $4 per 1 million characters.

You can customize the voice in the definition of the `voice` variable.
```python3
voice = texttospeech.VoiceSelectionParams(
    language_code='en-GB',
    name='en-GB-Neural2-B',
)
```
Go to [https://cloud.google.com/text-to-speech](https://cloud.google.com/text-to-speech) to try out different voices and languages. Below the text box, there is a button to show the json request.
E.g. to use an American english voice, replace `'en': ('en-GB', 'en-GB-Neural2-B'),` by `'en': ('en-US', 'en-US-Neural2-J'),`.
Also change the fallback Wavenet voice to the same voice a few lines further down:
```python3
voice = texttospeech.VoiceSelectionParams(
    language_code='en-GB',
    name='en-GB-Wavenet-B',
)
```
This voice is used if the Neural voice returns an error, e.g. because a sentence is too long.

On macOS, you can create a shortcut in the Finder with the following steps:
1. in Automator, create a new Quick Action. 
2. At the top, choose input as "PDF files" in "Finder". 
3. add a "Run Shell Script" action. Set shell to /bin/zsh and pass input as arguments. 
4. add the following code:
```bash
source ~/opt/miniconda3/etc/profile.d/conda.sh
conda activate paper2audio
python3 ~/path/to/paper2speech/main.py $1
```
5. save the action and give it a name, e.g. "Paper2Speech"

## Limitations
- captions of tables, figures are always read at the end of the page (because of the way Nougat has been trained)
- only works for English

## Future Work
- use GPT API to scan first page, detect names with special pronunciation, e.g. NVIDIA, IEEE, etc.
- read out figure caption before referenced in text
- add chapters to output audio file
- use proper parser (or GPT API) for inline math (likely Sympy Lark LaTeX parser)
