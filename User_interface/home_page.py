import os
import sys
import streamlit as st
from PIL import Image
import base64

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils import constants as CS
from utils import stringcontants as SC

def get_base64_image(image_path):
    """Encodes a local image to base64 for embedding in HTML."""
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

def show_homepage():
    try:
        st.markdown(
            """
            <div style="display: flex; align-items: center;">
                <h1 style="text-align: left; margin-right: 15px;">Welcome to the JobAgent Application</h1>
                <a href="https://github.com/shivarajmulimani/JobAgent" target="_blank">
                    <img src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png" width="40">
                    <b>View on GitHub</b>
                </a>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Display App Image
        app_image = Image.open(SC.README_IMAGE_1_PATH)
        # Display App Image
        st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
        st.image(app_image, width=300)
        st.markdown("</div>", unsafe_allow_html=True)

        st.info("👋 Hey there! This demo is just an experiment for learning and sharing knowledge. It’s only live for a few days, so feel free to explore while it lasts!, and do not forget to give feedback")

        # Introduction
        st.header("What is JobAgent Application?")
        st.write("This application allows you to search, match, and prepare your resume for jobs.")

        # How It Works
        st.header("How It Works")
        st.write("""
        1. The application first understands the uploaded resume.
        2. Then it lets you collect publicly available jobs from various internet sources using jobspy open source library.
        3. Later, the application analyzes what is missing in your resume and matches your resume against job requirements.
        4. Finally, it suggests updates to your resume if you qualify for relevant jobs.
        5. ***The collected resume, jobs and updated resume only remains for the duration of session, Application is designed with a intent to not store any mentioned data***.
        """)

        # Process Flow
        st.header("Process Flow")
        gif_base64 = get_base64_image(SC.README_IMAGE_2_PATH)

        st.markdown(
            f'<div style="text-align: center;">'
            f'<img src="data:image/gif;base64,{gif_base64}" width="500">'
            f'</div>',
            unsafe_allow_html=True
        )

        # Get Started
        st.header("Get Started")
        st.write("Use the menu on the left to switch between different sections.")

    except Exception as e:
        print("failed to show home page - ", e)