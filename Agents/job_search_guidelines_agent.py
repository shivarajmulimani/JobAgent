import os
import sys
from phi.agent import Agent, RunResponse
from phi.model.google import Gemini
from typing import List
from pydantic import BaseModel, Field

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils import constants as CS
from utils import stringcontants as SC


class JobSearchGuidelinesResponse(BaseModel):
    job_profile: str = Field(..., description="job title mentioned in the resume")
    alternatives: List[str] = Field(..., description="Alternative Job titles")


class JobSearchGuidelines:
    def __init__(self, resume):
        self.resume = resume
        self.agent = Agent(name=CS.JOB_SEARCHING_AGENT_NAME,
                           introduction=CS.JOB_SEARCHING_AGENT_INTRODUCTION,
                           model=Gemini(id=os.getenv("GEMINI_MODEL_CARD"), api_key=os.getenv("GEMINI_MODEL_API_KEY")),
                           # tools=[CsvTools(csvs=[csv_data])],
                           # tools=[PandasTools()]
                           markdown=True,
                           debug_mode=False,
                           show_tool_calls=False,
                           instructions=CS.JOB_SEARCHING_AGENT_INSTRUCTION,
                           response_model=JobSearchGuidelinesResponse,
                           structured_outputs=False
                           )

    def execute_agent(self, questions):
        response = None
        try:
            response = self.agent.run(f"question to answer - {questions} and below is the resume \n {self.resume}")
        except Exception as e:
            print("Failed to execute the agent - ", e)
        return response

    def run_agent(self, questions):
        try:
            response = None
            if self.resume:
                response = self.execute_agent(questions)
        except Exception as e:
            print("Failed to run resume updating agent - ", e)
        return response

if __name__ == "__main__":
    with open(SC.RESUME_DATA_FILE, 'r') as file:
        resume = file.read()
    questions = "What is the job profile mentioned in resume, also provide 2 alternatives to the job title?"
    jma = JobSearchGuidelines(resume)
    response = jma.run_agent(questions)
    print(response.content)