import os
import sys
import streamlit as st
import pandas as pd
import streamlit as st
import difflib
import re
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils import constants as CS
from utils import stringcontants as SC


def word_level_highlight(old_text, new_text):
    differ = difflib.SequenceMatcher(None, old_text, new_text)
    highlighted_text = ""

    for opcode, a0, a1, b0, b1 in differ.get_opcodes():
        old_part = old_text[a0:a1]
        new_part = new_text[b0:b1]

        if opcode == "replace":
            highlighted_text += f'<span style="background-color:#d9534f; color:white; padding:2px;">{old_part}</span>'
            highlighted_text += f'<span style="background-color:#5cb85c; color:white; padding:2px;">{new_part}</span>'
        elif opcode == "delete":
            highlighted_text += f'<span style="background-color:#d9534f; color:white; padding:2px;">{old_part}</span>'
        elif opcode == "insert":
            highlighted_text += f'<span style="background-color:#5cb85c; color:white; padding:2px;">{new_part}</span>'
        else:
            highlighted_text += old_part

    return highlighted_text


def updatedjobs_page():
    try:
        st.title("Updated Resume")
        # Streamlit UI
        st.title("File Difference Highlighter")

        file1 = st.session_state["file_content"]
        file2 = st.session_state["updated_resume"]

        highlighted_result = word_level_highlight(file1, file2)

        st.markdown(f'<div style="white-space:pre-wrap; font-family:monospace; font-size:14px;">{highlighted_result}</div>', unsafe_allow_html=True)

    except Exception as e:
        print("failed to show updated jobs page - ", e)
