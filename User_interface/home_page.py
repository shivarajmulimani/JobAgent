import os
import sys
import streamlit as st

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils import constants as CS
from utils import stringcontants as SC


def show_homepage():
    try:
        # Read the README.md file
        with open("../README.md", "r", encoding="utf-8") as file:
            readme_text = file.read()

            # Display the README content
            st.markdown(readme_text, unsafe_allow_html=True)

    except Exception as e:
        print("failed to show home page - ", e)