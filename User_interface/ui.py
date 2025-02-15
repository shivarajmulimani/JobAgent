import streamlit as st
import difflib
import os
import pandas as pd
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils import constants as CS
from utils import stringcontants as SC

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

    df = pd.read_csv(SC.SCRAPED_JOBS_DATA_FILE_CSV)

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
    st.title("Other Tab 2")
    st.write("Content for other tab 2 goes here.")
