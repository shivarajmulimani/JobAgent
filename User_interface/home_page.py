import os
import sys
import streamlit as st
from PIL import Image

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils import constants as CS
from utils import stringcontants as SC


def show_homepage():
    try:
        # Title
        st.markdown("<h1 style='text-align: left;'>Welcome to the JobAgent Application</h1>", unsafe_allow_html=True)

        # Display App Image
        app_image = Image.open("static/app_image.png")
        # Display App Image
        st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
        st.image(app_image, width=300)
        st.markdown("</div>", unsafe_allow_html=True)

        # Introduction
        st.header("What is JobAgent Application?")
        st.write("This application allows you to search, match, and prepare your resume for jobs.")

        # How It Works
        st.header("How It Works")
        st.write("""
        1. The application first understands the uploaded resume.
        2. Then it lets you collect publicly available jobs from various internet sources using jobspy open source library..
        3. Later, the application analyzes what is missing in your resume and matches your resume against job requirements.
        4. Finally, it suggests updates to your resume if you qualify for relevant jobs.
        """)

        # Process Flow
        st.header("Process Flow")
        flowchart = Image.open("static/flowchart.gif")
        st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
        st.image(flowchart, width=500)
        st.markdown("</div>", unsafe_allow_html=True)

        # Get Started
        st.header("Get Started")
        st.write("Use the menu on the left to switch between different sections.")

    except Exception as e:
        print("failed to show home page - ", e)