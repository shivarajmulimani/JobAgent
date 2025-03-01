import os
import sys
import pdfkit

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils import stringcontants as SC
# Manually set the path to wkhtmltopdf.exe (Windows only)
config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")

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