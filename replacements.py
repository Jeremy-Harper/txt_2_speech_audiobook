text_rules = [
    ("i\.e\.", 'that is'),
    ("e\.g\.", 'for example'),
    ("i\.i\.d\.", 'i i d'),
    ("Eq\.", 'Equation'),
    ("eq\.", 'equation'),
    ("Fig\.", 'Figure'),
    ("fig\.", 'figure'),
    ("vs\.", 'versus'),
    ("w\.r\.t\.", 'with respect to'),
    ("w\.r\.t", 'with respect to'),
]

math_rules = [
    (r"\\mathbb{R}\^{(.*?)}", r" R \1 "),
    (r"\\mathbb{C}\^{(.*?)}", r" C \1 "),
    (r"R\^{(.*?)}", r" R \1 "),
    (r"C\^{(.*?)}", r" C \1 "),
    (r"\\int_{(.*?)}\^{(.*?)}", r" integral from \1 to \2 of "),
    (r"\\int_(.*?)\^(.*?) ", r" integral from \1 to \2 of "),
    (r"\\frac{d(.*?)}{d(.*?)}", r" d \1 over d \2 of "),
    (r"\\dot{(.*?)}", r" \1 dot "),
    (r"\\ddot{(.*?)}", r" \1 double dot "),
    (r"\\partial_{(.*?)}", r" partial \1 "),
    (r"\\frac{(.*?)}{(.*?)}", r" \1 over \2 "),
    (r"\\mathcal{O}\((.*?)\)", r" order \1 "),
    (r"\\mathbf{(.*?)}", r" \1 "),
    (r"\\mathbb{(.*?)}", r" \1 "),
    (r"\\mathrm{(.*?)}", r" \1 "),
    (r"\\times", r" times "),
    (r"\^\{(.*?)\}", r" to the power of \1 "),
    (r"\^", r" to the power of "),
    (r"\\cdot", r" times "),
    (r"\\in", r" in "),
    (r"\\hat{(.*?)}", r" \1 hat "),
    (r"\\operatorname\*{arg\\,min}_{(.*?)}", r" arg min of \1 "),
    (r"\\operatorname\*{arg\\,max}_{(.*?)}", r" arg max of \1 "),
    (r"\\left\((.*?)\\right\)", r" \1 "),
    (r"\\left\[(.*?)\\right\]", r" \1 "),
    (r"\\left\{(.*?)\\right\}", r" \1 "),
    (r"\\left\|(.*?)\\right\|", r" \1 "),
    (r"\\sqrt{(.*?)}", r" square root of \1 "),
    (r"\\sum_{(.*?)}\^{(.*?)}", r" sum from \1 to \2 of "),
    (r"\\sum_(.*?)\^", r" sum from \1 to "),
    (r"\\prod_{(.*?)}\^{(.*?)}", r" product from \1 to \2 of "),
    (r"\\prod_(.*?)\^", r" product from \1 to "),
    (r"\\pi", r" pi "),
    (r"\\equiv", r" equivalent to "),
    (r"\\approx", r" approximately "),
    (r"\\neq", r" not equal to "),
    (r"\\leq", r" less than or equal to "),
    (r"\\geq", r" greater than or equal to "),
    (r"\\to", r" to "),
    (r"\\rightarrow", r" going to "),
    (r"\\leftarrow", r" is set to "),
    (r"\\mapsto", r" to "),
    (r"\\infty", r" infinity "),
    (r"\\alpha", r" alpha "),
    (r"\\beta", r" beta "),
    (r"\\gamma", r" gamma "),
    (r"\\delta", r" delta "),
    (r"\\epsilon", r" epsilon "),
    (r"\\eta", r" eta "),
    (r"\\theta", r" theta "),
    (r"\\kappa", r" kappa "),
    (r"\\lambda", r" lambda "),
    (r"\\mu", r" mu "),
    (r"\\nu", r" nu "),
    (r"\\xi", r" xi "),
    (r"\\rho", r" rho "),
    (r"\\sigma", r" sigma "),
    (r"\\tau", r" tau "),
    (r"\\phi", r" phi "),
    (r"\\chi", r" chi "),
    (r"\\psi", r" psi "),
    (r"\\omega", r" omega "),
    (r"\\Gamma", r" Gamma "),
    # ... Add more as required
]
