import os
import sys
import streamlit as st
import pandas as pd
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils import constants as CS
from utils import stringcontants as SC

def collectedjobs_page():
    try:
        st.title("Collected job Profiles")
        # Display dataframe
        st.write("Scrapped jobs data")
        st.dataframe(st.session_state["collected_jobs_df"])
        # Show summary statistics
        st.write("Data Summary:")
        # Identify numeric and categorical columns
        numeric_columns = st.session_state["collected_jobs_df"].select_dtypes(include=['number']).columns.tolist()
        categorical_columns = st.session_state["collected_jobs_df"].select_dtypes(exclude=['number']).columns.tolist()

        chart_type = st.radio("Select Chart Type:", ["Numerical Data", "Categorical Data"])

        if chart_type == "Numerical Data" and numeric_columns:
            selected_column = st.selectbox("Select a numeric column for bar chart", numeric_columns)
            st.write(f"### Bar Chart for {selected_column}")
            st.bar_chart(st.session_state["collected_jobs_df"][selected_column])

        elif chart_type == "Categorical Data" and categorical_columns:
            selected_column = st.selectbox("Select a categorical column for bar chart", categorical_columns)

            # Count occurrences of each category
            category_counts = st.session_state["collected_jobs_df"][selected_column].value_counts()

            # Show bar chart
            st.write(f"### Category Count for {selected_column}")
            st.bar_chart(category_counts)

        else:
            st.warning("No appropriate columns available for visualization.")

    except Exception as e:
        print("failed to show collected jobs page - ", e)