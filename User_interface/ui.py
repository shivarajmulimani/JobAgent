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

# Streamlit UI
st.sidebar.title("Navigation")
page = st.sidebar.radio("Choose a section", ["Home", "Updated Resume", "Collected job Profiles", "Analyse jobs with resume"])

if page == "Home":
    st.title("Welcome to the Application")
    st.write("This application allows you to compare text files and visualize differences in a Bitbucket-style format.")

    st.subheader("How It Works")
    st.write("1. The application reads two fixed text files from a directory.")
    st.write("2. It compares them line by line and highlights the differences.")
    st.write("3. Changes are displayed side by side, with additions, deletions, and modifications color-coded.")

    st.subheader("Process Flow")

    # Ensure correct GIF size
    st.image("giphy.gif", caption="Process Flow Animation", width=200)

    # Optional CSS fix for stubborn sizing issues
    st.markdown(
        """
        <style>
        img {
            max-width: 200px !important;
            height: auto !important;
        }
        </style>
        """,
        unsafe_allow_html=False
    )

    st.subheader("Get Started")
    st.write("Use the navigation on the left to switch between different sections.")

elif page == "Updated Resume":
    st.title("Updated Resume")

    # Fixed file names
    file1_path = SC.RESUME_DATA_FILE
    file2_path = os.path.join(SC.UPDATED_RESUME_STORAGE_PATH, "resume_content.txt")

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

    row_index = pd.DataFrame(selected_row).iloc[0, 0]

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
