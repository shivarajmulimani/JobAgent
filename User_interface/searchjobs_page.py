import os
import sys
import streamlit as st
import pandas as pd


sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils import constants as CS
from utils import stringcontants as SC
from Agents.job_search_guidelines_agent import JobSearchGuidelines
from job_search.jobspy_scraper import JobScraper

def highlight_text(text, bg_color="#D4EDDA", text_color="#155724"):
    return f"""
    <span style="
        background-color: {bg_color}; 
        padding: 4px 8px; 
        border-radius: 6px; 
        color: {text_color}; 
        font-weight: bold;
        font-size: 16px;
        display: inline-block;
        margin: 4px;">
        {text}
    </span>
    """


def searchjobs_page():
    try:
        st.markdown("## 📤 Upload your resume in .txt format")
        uploaded_file = st.file_uploader("Choose a .txt file", type=["txt"])
        if uploaded_file:
            st.session_state["uploaded_file"] = uploaded_file
            file_content = uploaded_file.read().decode("utf-8")
            st.session_state["file_content"] = file_content

        jsa = JobSearchGuidelines(st.session_state["file_content"])
        response = jsa.run_agent(CS.JOB_SEARCHING_AGENT_QUESTION)

        if response:
            job_profile = response.content.job_profile
            st.markdown("#### Job title :")
            highlighted_html = highlight_text(job_profile)
            st.markdown(highlighted_html, unsafe_allow_html=True)

            st.markdown("#### You can also consider these titles :")
            alternatives = response.content.alternatives
            highlighted_html = " ".join([highlight_text(text, "#FFF3CD", "#856404") for text in alternatives])
            st.markdown(highlighted_html, unsafe_allow_html=True)

            # Creating columns to limit text input width
            col1, col2, col3 = st.columns([1, 1, 1])  # Adjust column ratios for width control

            with col1:  # Centering the text input
                user_location = st.text_input("Enter your city:", "Bangalore")

            with col2:  # Centering the dropdown
                titles = [response.content.job_profile] + response.content.alternatives
                user_title = st.selectbox("Select job title:", titles, index=0)

            # Step 3: Show Confirmation Button
            if st.session_state["file_content"]:
                if st.button("Search for suitable jobs"):
                    scraper = JobScraper(
                        site_names=CS.SITE_NAMES,
                        search_term=user_title,
                        google_search_term=user_title,
                        job_type=CS.JOB_TYPE,
                        location=user_location,
                        results_wanted=CS.RESULTS_WANTED,
                        hours_old=CS.HOURS_OLD,
                        linkedin_fetch_description=CS.LINKED_FETCH_DESCRIPTION
                    )

                    with st.spinner("⏳ Processing... Please wait."):
                        scraper.scrape_jobs()
                        scraper.save_to_csv()
                        jobs_json = scraper.to_json()
                        st.session_state["collected_jobs_json"] = jobs_json  # Save in session state

                # ✅ Always display results if they exist, even after switching tabs
                if st.session_state["collected_jobs_json"]:
                    st.markdown("#### List of suitable jobs")
                    st.success(st.dataframe(pd.read_json(st.session_state["collected_jobs_json"])))

    except Exception as e:
        print("failed to show search jobs page - ", e)