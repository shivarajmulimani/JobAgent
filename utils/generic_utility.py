import os
import sys
import pdfkit
import streamlit as st
import fitz  # PyMuPDF for PDFs
from docx import Document
from io import BytesIO

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils import stringcontants as SC


# Check if OS is Windows and configure wkhtmltopdf
if os.name == "nt":  # 'nt' means Windows
    config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")
else:
    config = None  # No need for configuration on Linux/macOS

def write_to_file(filename, content):
    try:
        # Construct full file path
        file_path = os.path.join(SC.UPDATED_RESUME_STORAGE_PATH, filename)
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content + "\n")  # Ensure newline for formatting
        print(f"Successfully written to {filename}")
    except Exception as e:
        print(f"Error writing to file {filename}: {e}")

def save_html_to_pdf(html_content, pdf_path):
    try:
        """Convert HTML content to a PDF file using pdfkit."""
        options = {"enable-local-file-access": ""}
        pdfkit.from_string(html_content, pdf_path, options=options, configuration=config)

    except Exception as e:
        print("Failed to save updated resume - ", e)


def extract_text_from_file(uploaded_file):
    text_content = ""
    try:
        if uploaded_file is not None:
            file_extension = uploaded_file.name.split(".")[-1].lower()

            if file_extension == "pdf":
                text_content = extract_text_from_pdf(uploaded_file)
            elif file_extension == "docx":
                text_content = extract_text_from_docx(uploaded_file)
            elif file_extension == "txt":
                text_content = extract_text_from_txt(uploaded_file)
            else:
                st.error("Unsupported file format. Please upload a .txt, .pdf, or .docx file.")
                return None
        return text_content
    except Exception as e:
        print("failed to extract text from file - ", e)


def extract_text_from_pdf(uploaded_file):
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    return "\n".join([page.get_text() for page in doc])


def extract_text_from_docx(uploaded_file):
    doc = Document(BytesIO(uploaded_file.read()))
    return "\n".join([para.text for para in doc.paragraphs])


def extract_text_from_txt(uploaded_file):
    return uploaded_file.read().decode("utf-8")

