import streamlit as st
import difflib
import os
import pandas as pd
import sys
from st_aggrid import AgGrid, GridOptionsBuilder

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils import constants as CS
from utils import stringcontants as SC
from archestration.master import AgentArchestration
from Agents.job_search_guidelines_agent import JobSearchGuidelines
from job_search.jobspy_scraper import JobScraper

with open(SC.RESUME_DATA_FILE, 'r') as file:
    resume = file.read()
jobs = pd.read_json(SC.SCRAPED_JOBS_DATA_FILE_JSON)
jma = AgentArchestration(resume, jobs)

df = pd.read_csv(SC.SCRAPED_JOBS_DATA_FILE_CSV)

# Enable wide mode for better layout
st.set_page_config(layout="wide")

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

st.sidebar.title("Navigation")
page = st.sidebar.radio("Choose a section", ["Home", "Search jobs", "Collected job Profiles", "Analyse jobs with resume", "Updated Resume"])

if page == "Home":
    # Read the README.md file
    with open("../README.md", "r", encoding="utf-8") as file:
        readme_text = file.read()

        # Display the README content
        st.markdown(readme_text, unsafe_allow_html=True)

if page == "Search jobs":
    st.markdown("## 📤 Upload your resume in .txt format")
    uploaded_file = st.file_uploader("Choose a .txt file", type=["txt"])

    # Step 2: Read File in Background
    file_content = None
    if uploaded_file is not None:
        file_content = uploaded_file.read().decode("utf-8")
        jsa = JobSearchGuidelines(file_content)
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
    if file_content:
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

            st.markdown("#### List of suitable jobs")
            st.success(st.dataframe(pd.read_json(jobs_json)))

elif page == "Collected job Profiles":
    st.title("Collected job Profiles")
    # Display dataframe
    st.write("Scrapped jobs data")
    st.dataframe(df)
    # Show summary statistics
    st.write("Data Summary:")
    # Identify numeric and categorical columns
    numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
    categorical_columns = df.select_dtypes(exclude=['number']).columns.tolist()

    chart_type = st.radio("Select Chart Type:", ["Numerical Data", "Categorical Data"])

    if chart_type == "Numerical Data" and numeric_columns:
        selected_column = st.selectbox("Select a numeric column for bar chart", numeric_columns)
        st.write(f"### Bar Chart for {selected_column}")
        st.bar_chart(df[selected_column])

    elif chart_type == "Categorical Data" and categorical_columns:
        selected_column = st.selectbox("Select a categorical column for bar chart", categorical_columns)

        # Count occurrences of each category
        category_counts = df[selected_column].value_counts()

        # Show bar chart
        st.write(f"### Category Count for {selected_column}")
        st.bar_chart(category_counts)

    else:
        st.warning("No appropriate columns available for visualization.")

elif page == "Analyse jobs with resume":
    st.title("Analyse jobs with resume")
    # st.write("Content for other tab 2 goes here.")

    # Display dataframe
    st.write("Scrapped jobs data")
    # Configure AgGrid options
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_selection("single")  # Allows single-row selection
    grid_options = gb.build()

    # Display interactive grid
    grid_response = AgGrid(df, gridOptions=grid_options, height=300, fit_columns_on_grid_load=True)

    selected_row = grid_response.get("selected_rows", [])  # Handle None case
    # import pdb;pdb.set_trace()
    if selected_row is not None and not selected_row.empty:
        row_index = pd.DataFrame(selected_row).iloc[0, 0]
    else:
        row_index = None

    if row_index:  # Ensure a row is selected
        # Find the actual index using the "id" column
        unique_col = "id"  # Change this if there's a better unique column
        row = df[df['id'] == row_index]
        st.write("**Selected job:**", row)

        response = jma.job_match_individual(row_index)

        if response:
            st.markdown("### ⭐ Rating Score out of 10", unsafe_allow_html=True)
            st.write(response.get('rating'))

            st.markdown("### 📝 Reason for Score ", unsafe_allow_html=True)
            # st.write(response.get('justification'))
            # Custom CSS for bullet points in yellowish-orange color
            st.markdown(
                """
                <style>
                .bullet-list {
                    color: #FFA500;  /* Yellowish-orange color */
                    font-size: 18px; /* Adjust font size */
                }
                </style>
                """,
                unsafe_allow_html=True
            )

            # Display bullet points
            st.markdown("<ul>", unsafe_allow_html=True)
            for item in response.get('justification'):
                st.markdown(f'<li class="bullet-list">{item}</li>', unsafe_allow_html=True)
            st.markdown("</ul>", unsafe_allow_html=True)

            resume_text = response.get('updated resume')
            # st.write(response.get('updated resume'))

            # Properly formatted HTML for text visibility
            resume_html = f"""
                <div style="
                    border: 2px solid #ccc; 
                    border-radius: 10px; 
                    padding: 15px; 
                    background-color: #fff; 
                    color: #333;  /* Ensure visible text */
                    font-family: monospace; 
                    white-space: pre-wrap;  /* Preserve spaces & new lines */
                    font-size: 16px;
                    line-height: 1.6;
                    overflow-x: auto;">
            {resume_text}
                </div>
            """

            # Display resume with styling
            st.markdown("### 📄 Updated resume", unsafe_allow_html=True)
            st.markdown(resume_html, unsafe_allow_html=True)

            # Convert text to bytes for download
            resume_bytes = resume_text.encode("utf-8")

            # Provide download button
            st.download_button(
                label="📥 Download Resume",
                data=resume_bytes,
                file_name="resume.txt",
                mime="text/plain"
            )

elif page == "Updated Resume":
    st.title("Updated Resume")

    # Fixed file names
    file1_path = SC.RESUME_DATA_FILE
    file2_path = os.path.join(SC.UPDATED_RESUME_STORAGE_PATH, "205cf17c-0839-4ff8-be37-bba8723196c9.txt")

    text1 = read_file(file1_path)
    text2 = read_file(file2_path)

    if text1 and text2:
        file1_diff, file2_diff = word_level_diff(text1, text2)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(file1_diff, unsafe_allow_html=True)
        with col2:
            st.markdown(file2_diff, unsafe_allow_html=True)
    else:
        st.error("One or both files are missing in the directory.")