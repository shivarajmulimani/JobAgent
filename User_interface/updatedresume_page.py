import os
import sys
import streamlit as st
import pandas as pd
import difflib

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils import constants as CS
from utils import stringcontants as SC


def read_file(filepath):
    """Reads a text file from a fixed directory and returns its content as a string."""
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        return ""


def word_level_diff(text1, text2):
    """Generates a Bitbucket-style side-by-side code diff with proper color coding."""
    text1_lines = text1.splitlines(keepends=True)
    text2_lines = text2.splitlines(keepends=True)

    matcher = difflib.SequenceMatcher(None, text1_lines, text2_lines)
    file1_diff, file2_diff = [], []

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        for line in text1_lines[i1:i2]:
            if tag == "replace":
                file1_diff.append(f'<span style="background-color:#ffeeba; color:black;">{line}</span>')
            elif tag == "delete":
                file1_diff.append(
                    f'<span style="background-color:#f8d7da; color:red; text-decoration: line-through;">{line}</span>')
            else:
                file1_diff.append(line)

        for line in text2_lines[j1:j2]:
            if tag == "replace":
                file2_diff.append(f'<span style="background-color:#ffeeba; color:black;">{line}</span>')
            elif tag == "insert":
                file2_diff.append(f'<span style="background-color:#d4edda; color:green;">{line}</span>')
            else:
                file2_diff.append(line)

    return (
        '<div style="white-space: pre-wrap; font-family: monospace;">' + "<br>".join(file1_diff) + '</div>',
        '<div style="white-space: pre-wrap; font-family: monospace;">' + "<br>".join(file2_diff) + '</div>'
    )


def updatedjobs_page():
    try:
        st.title("Updated Resume")

        # Fixed file names
        # file1_path = st.session_state["file_content"]
        # file2_path = st.session_state["updated_resume"]

        text1 = st.session_state["file_content"]
        text2 = st.session_state["updated_resume"]

        if text1 and text2:
            file1_diff, file2_diff = word_level_diff(text1, text2)

            col1, col2 = st.columns(2)
            with col1:
                st.markdown(file1_diff, unsafe_allow_html=True)
            with col2:
                st.markdown(file2_diff, unsafe_allow_html=True)
        else:
            st.error("One or both files are missing in the directory.")
    except Exception as e:
        print("failed to show updated jobs page - ", e)