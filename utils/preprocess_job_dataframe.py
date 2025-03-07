import pandas as pd
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils import constants as CS
from utils import stringcontants as SC

def preprocess_job_df(df):
    df = df[CS.USEFUL_COLUMNS]
    # Ensure 'Date' is converted to datetime
    df['date_posted'] = pd.to_datetime(df['date_posted'], unit='ms')
    # Format date properly (optional)
    df['date_posted'] = df['date_posted'].dt.strftime('%Y-%m-%d')

    # df['company_url'] = df['company_url'].apply(lambda x: f'<a href="{x}" target="_blank">{x}</a>')

    # df['job_url_direct'] = df['job_url_direct'].apply(lambda x: f'<a href="{x}" target="_blank">{x}</a>')
    return df