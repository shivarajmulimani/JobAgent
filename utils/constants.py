JOB_SEARCHING_AGENT_NAME = "Job searching"
JOB_SEARCHING_AGENT_INTRODUCTION = "you will be given with a resume and set of questions, you will be answering to the questions"

JOB_SEARCHING_AGENT_INSTRUCTION = ["First understand the resume",
                                  "Understand the questions",
                                  "Provide answer to question with no explaination",
                                  "Along with answer you can suggest some more similar titles"
                                  "return response in json"]

JOB_SEARCHING_AGENT_QUESTION = "What is the job profile mentioned in resume, also provide 2 alternatives to the job title?"

#######################################################################################################################

JOB_MATCHING_AGENT_NAME = "Job matching"
JOB_MATCHING_AGENT_INTRODUCTION = "you will be given with a resume and job application you task is to tell wether given job application suitable to the resume ot not"

JOB_MATCHING_AGENT_INSTRUCTION = ["First understand the resume",
                                  "understand the skills mentioned in resume",
                                  "Then understand the job application requirements",
                                  "Then give a rating between 1 to 10, max rating if resume and job application matches else minimum rating",
                                  "only return rating and justification in few points"
                                  "return response in json with rating and justification keys"]

#######################################################################################################################

RESUME_UPDATE_AGENT_NAME = "Resume updating"
RESUME_UPDATE_AGENT_INTRODUCTION = "you will be given with a resume and what is missing with respect to new job requirement you must suggest the resume edits"

RESUME_UPDATE_AGENT_INSTRUCTION = ["First understand the resume",
                                  "understand the gaps mentioned in justification section",
                                  "Then decide what needs to be added with minimal changes",
                                  "Resume should sound good and contenful",
                                  "only return the updated resume maintain the same format and indents and new lines"
                                  "return response in text"
    ]
#######################################################################################################################

SITE_NAMES = ["linkedin", "glassdoor", "google"]
JOB_TYPE = "fulltime"
LOCATION = " India, Bangalore"
RESULTS_WANTED = 5
HOURS_OLD = 72
LINKED_FETCH_DESCRIPTION = True
USEFUL_COLUMNS = ['title', 'company', 'job_type', 'location', 'job_level', 'description', 'company_industry', 'max_amount', 'company_url', 'date_posted' ,'job_url_direct', 'id']