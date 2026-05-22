import fitz  # PyMuPDF

def extract_text(file):
    """
    Supports:
    - Streamlit uploaded file
    - Local file path (for testing)
    """

    # Case 1: file path (string)
    if isinstance(file, str):
        doc = fitz.open(file)

    # Case 2: uploaded file (Streamlit)
    else:
        doc = fitz.open(stream=file.read(), filetype="pdf")

    text = ""

    for page in doc:
        text += page.get_text("text") + "\n"

    # 🔥 cleanup
    text = text.replace("\n\n", "\n")
    text = text.strip()

    return text


# ✅ Now this will work

