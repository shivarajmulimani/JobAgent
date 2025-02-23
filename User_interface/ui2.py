import os
import sys
import streamlit as st

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from User_interface.home_page import show_homepage
from User_interface.searchjobs_page import searchjobs_page

# Enable wide mode for better layout
st.set_page_config(layout="wide")

class UI:
    def __init__(self):
        if "uploaded_file" not in st.session_state:
            st.session_state["uploaded_file"] = None

        if "file_content" not in st.session_state:
            st.session_state["file_content"] = None

        if "collected_jobs_json" not in st.session_state:
            st.session_state["collected_jobs_json"] = None
            st.session_state["collected_jobs_df"] = None

    def start_ui(self):
        st.sidebar.title("Navigation")
        page = st.sidebar.radio("Choose a section",
                                ["Home",
                                 "Search jobs",
                                 "Collected job Profiles",
                                 "Analyse jobs with resume",
                                 "Updated Resume"])
        if page == "Home":
            show_homepage()

        if page == "Search jobs":
            searchjobs_page()


if __name__ == "__main__":
    ui_obj = UI()
    ui_obj.start_ui()