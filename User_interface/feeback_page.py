import streamlit as st
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils import constants as CS
from utils import stringcontants as SC


# Function to save feedback to a file
def save_feedback(feedback_text):
    with open(SC.FEEDBACK_STORAGE_PATH, "a") as file:
        file.write(feedback_text + "\n---\n")  # Separate entries with '---'

# Function to read all feedback from the file
def load_feedback():
    try:
        with open(SC.FEEDBACK_STORAGE_PATH, "r") as file:
            return file.read().strip().split("\n---\n")  # Split entries by '---'
    except FileNotFoundError:
        return []  # Return empty list if file doesn't exist


def feedback_page():
    try:
        st.title("Feedback Page")
        # Feedback input
        feedback = st.text_area("Enter your feedback:")

        # Submit button
        if st.button("Submit Feedback"):
            if feedback.strip():  # Ensure non-empty feedback
                save_feedback(feedback)
                st.success("Thank you for your feedback!")
                st.write("\n\n")

        # Show all feedback
        st.subheader("Past Feedbacks:")
        all_feedback = load_feedback()

        if all_feedback:
            for i, fb in enumerate(reversed(all_feedback), 1):  # Show latest first
                st.markdown(f'<p style="font-size:14px; background-color:#0073e6; color:#ffffff; padding:10px; border-radius:5px;">{fb}</p>',
                    unsafe_allow_html=True
                )
        else:
            st.write("No feedback submitted yet.")

    except Exception as e:
        print("Failed to show feedback page - ", e)
