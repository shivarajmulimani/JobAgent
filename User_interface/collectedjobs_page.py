import os
import sys
import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from babel.numbers import format_currency

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

def collectedjobs_page():
    try:
        df = st.session_state["collected_jobs_df"]
        st.title("📊 Job Market Insights Dashboard")
        st.write("")  # Adds a small space
        st.write("")  # Adds more space

        try:
            df['date_posted'] =  pd.to_datetime(df['date_posted'])
            st.header("🔹 Key Job Statistics")
            total_jobs = len(df)
            max_salary_value = df['max_amount'].max()
            # Format currency for India (INR)
            max_salary = format_currency(max_salary_value, currency="INR", locale="hi_IN")
            latest_job_posted = df['date_posted'].max().strftime("%Y-%m-%d")

            st.markdown(
                f"""
                <style>
                    .card-container {{
                        display: flex;
                        justify-content: center;
                        gap: 20px;
                        margin-top: 20px;
                    }}
                    .card {{
                        background: linear-gradient(135deg, #E3F2FD, #BBDEFB); /* Soft Blue */
                        padding: 20px;
                        border-radius: 12px;
                        text-align: center;
                        box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
                        font-size: 20px;
                        font-weight: bold;
                        color: #004085;
                        min-width: 200px;
                        flex: 1;
                    }}
                    .card:nth-child(2) {{ background: linear-gradient(135deg, #E8F5E9, #C8E6C9); color: #155724; }} /* Soft Green */
                    .card:nth-child(3) {{ background: linear-gradient(135deg, #FFF3CD, #FFE082); color: #856404; }} /* Soft Yellow */
                    @media (max-width: 768px) {{
                        .card-container {{ flex-direction: column; align-items: center; }}
                    }}
                </style>

                <div class="card-container">
                    <div class="card">📌 Total Jobs<br>{total_jobs}</div>
                    <div class="card">💰 Max Salary<br>{max_salary}</div>
                    <div class="card">🆕 Latest Job Posted<br>{latest_job_posted}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
            st.write("")  # Adds a small space
            st.write("")  # Adds more space
            st.write("")  # Adds a small space
            st.write("")  # Adds more space
        except Exception as e:
            print("failed to show key job statistics - ", e)

        # 🚀 **Job Distribution by Industry**
        try:
            st.header("🛠️ Job Distribution by Industry")
            industry_counts = df['company_industry'].value_counts()
            fig_industry = px.bar(
                industry_counts,
                x=industry_counts.index,
                y=industry_counts.values,
                labels={'x': 'Industry', 'y': 'Number of Jobs'},
                title="Industry-wise Job Count",
                color=industry_counts.index,
                text=industry_counts.values
            )
            st.plotly_chart(fig_industry)
            st.write("")  # Adds a small space
            st.write("")  # Adds more space
            st.write("")  # Adds a small space
            st.write("")  # Adds more space
        except Exception as e:
            print("Failed to show JOb distribution by Industry - ", e)

        # 🚀 **Salary Trends Over Time**
        try:
            st.header("📈 Salary Trends Over Time")
            df['date_posted'] = pd.to_datetime(df['date_posted'], errors='coerce')
            # Fill NaN values with 0
            df['max_amount'] = df['max_amount'].fillna(0)

            # Group by date and calculate the mean
            salary_trend = df.groupby(df['date_posted'].dt.date)['max_amount'].mean()

            print(salary_trend)
            fig_salary = px.line(
                salary_trend,
                x=salary_trend.index,
                y=salary_trend.values,
                labels={'x': 'Date', 'y': 'Average Salary'},
                markers=True
                # title="Salary Trends Over Time"
            )
            st.plotly_chart(fig_salary)
            st.write("")  # Adds a small space
            st.write("")  # Adds more space
            st.write("")  # Adds a small space
            st.write("")  # Adds more space
        except Exception as e:
            print("failed to show salary trends - ", e)

        # 🚀 **Map of Job Locations**
        try:
            # ✅ Group by date to count job postings
            job_trend = df.groupby(df['date_posted'].dt.date).size().reset_index(name='job_count')
            # ✅ Create a trend line chart
            fig_trend = px.line(
                job_trend,
                x='date_posted',
                y='job_count',
                labels={'date_posted': 'Date', 'job_count': 'Number of Job Postings'},
                title="📅 Job Postings Over Time",
                markers=True
            )
            # ✅ Show in Streamlit
            st.plotly_chart(fig_trend)
            st.write("")  # Adds a small space
            st.write("")  # Adds more space
            st.write("")  # Adds a small space
            st.write("")  # Adds more space
        except Exception as e:
            print("failed to show job location map - ", e)

        # company names
        try:
            st.header("🏢 Company names")
            # 🔹 Remove duplicates and create a new DataFrame
            df_unique = df.drop_duplicates(subset=["company"]).reset_index(drop=True)

            # Define number of columns per row
            cols_per_row = 8  # Adjust as needed

            # Convert company names & URLs into table format
            company_list = df_unique[["company", "company_url"]].values.tolist()
            rows = [company_list[i:i + cols_per_row] for i in range(0, len(company_list), cols_per_row)]

            # Generate HTML table with clickable links or plain text if URL is missing
            table_html = "<table style='width:100%; border-collapse: collapse;'>"
            for row in rows:
                table_html += "<tr>"
                for company, url in row:
                    table_html += "<td style='border: 1px solid #ddd; padding: 10px; text-align: center; font-size: 18px;'>"
                    if pd.notna(url):  # If URL exists, make it clickable
                        table_html += f"<a href='{url}' target='_blank' style='text-decoration: none; color: #0078D4;'>{company}</a>"
                    else:  # If URL is missing, show plain text in gray
                        table_html += f"<span style='color: gray;'>{company}</span>"
                    table_html += "</td>"
                table_html += "</tr>"
            table_html += "</table>"

            # Display the table in Streamlit
            st.markdown(table_html, unsafe_allow_html=True)
            st.write("")  # Adds a small space
            st.write("")  # Adds more space

        except Exception as e:
            print("filed to show company names - ", e)

        # 🚀 **Word Cloud for Job Descriptions**
        try:
            st.header("🔎 Common Words in Job Descriptions")
            text = " ".join(df['description'])
            wordcloud = WordCloud(width=800, height=400, background_color="black").generate(text)
            fig, ax = plt.subplots()
            ax.imshow(wordcloud, interpolation='bilinear')
            ax.axis("off")
            st.pyplot(fig)
            st.write("")  # Adds a small space
            st.write("")  # Adds more space
        except Exception as e:
            print("failed to show common words in job description - ", e)


    except Exception as e:
        print("failed to show collected jobs page - ", e)