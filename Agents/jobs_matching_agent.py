import os
import sys
import pandas as pd
from phi.agent import Agent, RunResponse
from phi.model.google import Gemini
from typing import List
from pydantic import BaseModel, Field


sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils import constants as CS
from utils import api_keys as AK
from utils import stringcontants as SC


class JobmatchResponse(BaseModel):
    rating: int = Field(..., description="Rating of the job matching")
    justification: List[str] = Field(..., description="Job rating justification in few points")


class JobMatchingAgent:
    def __init__(self, resume):
        self.resume = resume
        self.agent = Agent(name=CS.JOB_MATCHING_AGENT_NAME,
                           introduction=CS.JOB_MATCHING_AGENT_INTRODUCTION,
                           model=Gemini(id=AK.GEMINI_MODEL_CARD, api_key=AK.GEMINI_MODEL_API_KEY),
                           # tools=[CsvTools(csvs=[csv_data])],
                           # tools=[PandasTools()]
                           markdown=False,
                           debug_mode=False,
                           show_tool_calls=False,
                           instructions=CS.JOB_MATCHING_AGENT_INSTRUCTION,
                           response_model=JobmatchResponse,
                           structured_outputs=True
                           )

    def execute_agent(self, job_description):
        response = None
        try:
            response = self.agent.run(f"resume - {self.resume}, and job application is - {job_description}")
        except Exception as e:
            print("Failed to execute the agent - ", e)
        return response

    def run_agent(self, job_description):
        try:
            response = None
            if job_description:
                response = self.execute_agent(job_description)
        except Exception as e:
            print("Failed to run job matching agent - ", e)
        return response

if __name__ == "__main__":
    with open(SC.RESUME_DATA_FILE, 'r') as file:
        resume = file.read()
    jobs = pd.read_json(SC.SCRAPED_JOBS_DATA_FILE_JSON)

    jma = JobMatchingAgent(resume)
    for index, row in jobs.iterrows():
        response = None
        job_description = row['description']
        job_url = row['job_url']
        title = row['title']
        company = row['company']
        response = jma.run_agent(job_description)
        print(company)
        print(title)
        if response:
            print(response.content.rating)
            print(response.content.justification)
    print('-' * 30)