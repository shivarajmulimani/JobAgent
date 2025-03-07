import os
import sys
import pandas as pd
from phi.agent import Agent, RunResponse
from phi.model.google import Gemini
from pydantic import BaseModel, Field


sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils import constants as CS
from utils import stringcontants as SC


class ResumeUpdateResponse(BaseModel):
    resume: str = Field(..., description="Resume of data scientist")


class ResumeUpdateAgent:
    def __init__(self, resume):
        self.resume = resume
        self.agent = Agent(name=CS.RESUME_UPDATE_AGENT_NAME,
                           introduction=CS.RESUME_UPDATE_AGENT_INTRODUCTION,
                           model=Gemini(id=os.getenv("GEMINI_MODEL_CARD"), api_key=os.getenv("GEMINI_MODEL_API_KEY")),
                           markdown=True,
                           debug_mode=False,
                           show_tool_calls=False,
                           instructions=CS.RESUME_UPDATE_AGENT_INSTRUCTION,
                           # response_model=ResumeUpdateResponse,
                           # structured_outputs=False
                           )

    def execute_agent(self, resume_justification):
        response = None
        try:
            response = self.agent.run(f"resume - {self.resume}, and requirements justification is - {resume_justification}")
        except Exception as e:
            print("Failed to execute the agent - ", e)
        return response

    def run_agent(self, resume_justification):
        try:
            response = None
            if resume_justification:
                response = self.execute_agent(resume_justification)
        except Exception as e:
            print("Failed to run resume updating agent - ", e)
        return response

if __name__ == "__main__":
    with open(SC.RESUME_DATA_FILE, 'r') as file:
        resume = file.read()
    job_justification = ''''The candidate has a strong background in AI and data science, with experience in various relevant technologies (Python, ML, NLP, AWS, GCP).', 
                            'However, the resume lacks specific experience in the healthcare industry and oncology, which are crucial requirements for this role.', 
                            "The candidate's projects, while impressive, don't directly translate to the specific needs of working with large patient-level healthcare RWD and multi-omics data.", 
                            'The required experience of 6+ years in the life science or biotech industry in a Data Science role is not explicitly demonstrated in the resume.'''
    jma = ResumeUpdateAgent(resume)
    response = jma.run_agent(job_justification)
    print(response.content)