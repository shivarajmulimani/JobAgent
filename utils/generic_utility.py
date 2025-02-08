import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils import stringcontants as SC


def write_to_file(filename, content):
    try:
        # Construct full file path
        file_path = os.path.join(SC.UPDATED_RESUME_STORAGE_PATH, filename)
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content + "\n")  # Ensure newline for formatting
        print(f"Successfully written to {filename}")
    except Exception as e:
        print(f"Error writing to file {filename}: {e}")