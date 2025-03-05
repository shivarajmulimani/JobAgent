import os
import sys
import streamlit as st
import pandas as pd
import streamlit as st
import difflib
import diff_match_patch as dmp_module
import re


sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils.generic_utility import save_html_to_pdf
from utils.stringcontants import UPDATED_RESUME_PATH


def generate_inline_diff(text1, text2):
    dmp = dmp_module.diff_match_patch()
    diffs = dmp.diff_main(text1, text2)
    dmp.diff_cleanupSemantic(diffs)

    # Format diff output with HTML while preserving new lines
    formatted_diff = []
    updated_content = []
    for op, data in diffs:
        data = re.sub(r"\n+", "<br>", data)  # Replace multiple new lines dynamically

        if op == 1:  # Addition (green)
            formatted_diff.append(f'<span style="background-color: #5cb85c;">{data}</span>')
            updated_content.append(data)
        elif op == -1:  # Deletion (red)
            formatted_diff.append(f'<span style="background-color: #d9534f; text-decoration: line-through;">{data}</span>')
        else:  # No Change
            formatted_diff.append(data)
            updated_content.append(data)

    diff_out = "".join(formatted_diff)
    updated_out = "".join(updated_content)
    return diff_out, updated_out


def updatedjobs_page():
    try:
        st.title("Updated Resume")
        file1 = st.session_state["file_content"]
        file2 = st.session_state["updated_resume"]

        if file1 and file2:
            diff_output, updated_out = generate_inline_diff(file1, file2)
            st.markdown(f"<pre>{diff_output}</pre>", unsafe_allow_html=True)

            # Apply Font Style
            styled_html = f"""
            <html>
            <head>
                <style>
                    body {{
                        font-family: 'Calibri', serif;
                        font-size: 18px;
                        line-height: 1.5;
                    }}
                    p {{
                        margin-bottom: 10px;
                    }}
                </style>
            </head>
            <body>
            {updated_out}
            </body>
            </html>
            """

            # Generate PDF
            save_html_to_pdf(styled_html, UPDATED_RESUME_PATH)

            # Provide a download button
            downloaded = False
            with open(UPDATED_RESUME_PATH, "rb") as pdf_file:
                st.download_button(
                    label="Download Diff as PDF",
                    data=pdf_file,
                    file_name="updated_file.pdf",
                    mime="application/pdf"
                )
                downloaded = True

            if downloaded and os.path.exists(UPDATED_RESUME_PATH):
                os.remove(UPDATED_RESUME_PATH)
                print("File deleted successfully.")
            else:
                print("File does not exist.")

    except Exception as e:
        print("failed to show updated jobs page - ", e)
