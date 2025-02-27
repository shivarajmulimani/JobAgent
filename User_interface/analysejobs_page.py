import os
import sys
import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils import constants as CS
from utils import stringcontants as SC
from archestration.master import AgentArchestration

# with open(SC.RESUME_DATA_FILE, 'r') as file:
#     resume = file.read()
# jobs = pd.read_json(SC.SCRAPED_JOBS_DATA_FILE_JSON)
# jma = AgentArchestration(resume, jobs)

def analysejobs_page():
    try:
        resume = st.session_state["file_content"]
        jobs = st.session_state["collected_jobs_df"]
        jma = AgentArchestration(resume, jobs)
        st.title("Analyse jobs with resume")

        # Display dataframe
        st.write("Scrapped jobs data")
        # Configure AgGrid options
        gb = GridOptionsBuilder.from_dataframe(jobs)
        gb.configure_selection("single")  # Allows single-row selection
        grid_options = gb.build()

        # Display interactive grid
        grid_response = AgGrid(jobs, gridOptions=grid_options, height=300, fit_columns_on_grid_load=True)
        st.write("Please select interested job")

        selected_row = grid_response.get("selected_rows", [])  # Handle None case
        # import pdb;pdb.set_trace()
        if selected_row is not None and not selected_row.empty:
            row_index = pd.DataFrame(selected_row).iloc[0, -1]
        else:
            row_index = None

        if row_index:  # Ensure a row is selected
            # Find the actual index using the "id" column
            unique_col = "id"  # Change this if there's a better unique column
            row = jobs[jobs['id'] == row_index]
            st.write("**Selected job:**", row)

            with st.spinner("🔍📄 Analysing job requirement and resume..."):
                response = jma.job_match_individual(row_index)

            if response:
                st.markdown("### ⭐ Rating Score out of 10", unsafe_allow_html=True)
                st.write(response.get('rating'))

                st.markdown("### 📝 Reason for Score ", unsafe_allow_html=True)

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
                st.session_state["updated_resume"] = resume_text
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
                st.download_button(label="📥 Download Resume", data=resume_bytes, file_name="resume.txt", mime="text/plain")

    except Exception as e:
        print("failed to show Analyse jobs page - ", e)