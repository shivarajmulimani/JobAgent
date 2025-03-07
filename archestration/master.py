import os
import sys
import uuid
import pandas as pd


sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from Agents.jobs_matching_agent import JobMatchingAgent
from Agents.resume_update_agent import ResumeUpdateAgent
from utils.generic_utility import *
from utils import constants as CS
from utils import stringcontants as SC

class AgentArchestration:
    def __init__(self, resume, jobs):
        self.resume = resume
        self.jobs = jobs
        self.job_matching_agent = JobMatchingAgent(resume)
        self.resume_updating_agent = ResumeUpdateAgent(resume)

    def execute_agents(self):
        try:
            for index, row in self.jobs.iterrows():
                match_response = None
                resume_update_response = None
                job_description = row['description']
                title = row['title']
                company = row['company']
                match_response = self.job_matching_agent.run_agent(job_description)
                print(company)
                print(title)
                if match_response:
                    print(match_response.content.rating)
                    print(match_response.content.justification)
                    resume_update_response = self.resume_updating_agent.run_agent(match_response.content.justification)
                    print(resume_update_response.content)
                    filename = str(uuid.uuid4()) + ".txt"
                    write_to_file(filename, resume_update_response.content)
                break
        except Exception as e:
            print("Failed to execute the agent - ", e)

    def job_match_individual(self, id, store_resume=False):
        try:
            response = dict()
            # Filter by a specific index
            row = self.jobs[self.jobs['id'] == id]  # Get all columns for index
            match_response = None
            resume_update_response = None
            job_description = row['description'].values[0]
            title = row['title'].values[0]
            company = row['company'].values[0]
            match_response = self.job_matching_agent.run_agent(job_description)
            if match_response:
                response['rating'] = match_response.content.rating
                response['justification'] = match_response.content.justification
                resume_update_response = self.resume_updating_agent.run_agent(match_response.content.justification)
                response['updated resume'] = resume_update_response.content
                if store_resume:
                    filename = str(uuid.uuid4()) + ".txt"
                    write_to_file(filename, resume_update_response.content)
        except Exception as e:
            print(e)
        return response

    def job_match_bulk(self):
        try:
            pass
        except Exception as e:
            print(e)

    def run_agent(self, resume_justification):
        try:
            response = None
            if resume_justification:
                self.execute_agents(resume_justification)
        except Exception as e:
            print("Failed to run resume updating agent - ", e)
        return response

if __name__ == "__main__":
    with open(SC.RESUME_DATA_FILE, 'r') as file:
        resume = file.read()
    jobs = pd.read_json(SC.SCRAPED_JOBS_DATA_FILE_JSON)
    jma = AgentArchestration(resume, jobs)
    # jma.execute_agents()
    response = jma.job_match_individual("gd-1009615110820")
    print(response)