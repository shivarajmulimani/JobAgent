import json
from pprint import pprint
from linkedin_api import Linkedin


class LinkedInAPI:
    def __init__(self, credentials):
        self.linkedin = Linkedin(credentials["username"], credentials["password"])

    def search_jobs(self):
        try:
            jobs = self.linkedin.search_jobs(limit=10)
            return jobs
        except Exception as e:
            print("failed to search jobs - ", e)


def unit_test():
    with open("credentials.json", "r") as file:
        credentials = json.load(file)

    api = LinkedInAPI(credentials)
    jobs = api.search_jobs()
    print(jobs)

if __name__ == "__main__":
    unit_test()