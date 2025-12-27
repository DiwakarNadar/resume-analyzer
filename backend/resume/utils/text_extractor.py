import requests
import io
import pdfplumber
import docx
from urllib.parse import urlparse


def extract_text_from_pdf(content: bytes) -> str:
    text = ""
    with pdfplumber.open(io.BytesIO(content)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.strip()


def extract_text_from_docx(content: bytes) -> str:
    text = ""
    doc = docx.Document(io.BytesIO(content))
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text.strip()


def extract_text_from_file(file_url: str) -> str:
    """
    Downloads file from signed URL and extracts text
    Supports PDF and DOCX
    """

    # Parse URL safely (ignore ?token=...)
    parsed = urlparse(file_url)
    clean_path = parsed.path.lower()

    response = requests.get(file_url)
    response.raise_for_status()

    content = response.content

    if clean_path.endswith(".pdf"):
        return extract_text_from_pdf(content)

    if clean_path.endswith(".docx"):
        return extract_text_from_docx(content)

    raise ValueError("Unsupported file format")
