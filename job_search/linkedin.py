import json
from pprint import pprint
from linkedin_api import Linkedin

with open("credentials.json", "r") as f:
    credentials = json.load(f)


# Authenticate using any Linkedin user account credentials
api = Linkedin(credentials["username"], credentials["password"])

# GET a profile
profile = api.search_jobs(keywords="Data science", limit=5)

# GET a profiles contact info
# contact_info = api.get_profile_contact_info('billy-g')

# GET 1st degree connections of a given profile
# connections = api.get_profile_connections('1234asc12304')

pprint(profile)