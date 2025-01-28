import csv
import json
import os
import sys
from jobspy import scrape_jobs
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils import stringcontants as SC


class JobScraper:
    def __init__(self, site_names, search_term, job_type, location, results_wanted, hours_old, google_search_term=None, linkedin_fetch_description=False):
        """
        Initialize the JobScraper with scraping configuration.
        """
        self.site_names = site_names
        self.search_term = search_term
        self.job_type = job_type
        self.location = location
        self.results_wanted = results_wanted
        self.hours_old = hours_old
        self.google_search_term = google_search_term
        self.linkedin_fetch_description = linkedin_fetch_description
        self.jobs = None

    def scrape_jobs(self):
        """
        Scrape jobs based on the initialized parameters.
        """
        try:
            self.jobs = scrape_jobs(
                site_name=self.site_names,
                search_term=self.search_term,
                google_search_term=self.google_search_term,
                job_type=self.job_type,
                location=self.location,
                results_wanted=self.results_wanted,
                hours_old=self.hours_old,
                linkedin_fetch_description=self.linkedin_fetch_description
            )
            print(f"Found {len(self.jobs)} jobs")
        except Exception as e:
            print("Failed to search jobs")

    def save_to_csv(self, filename=SC.SCRAPED_JOBS_DATA_FILE_CSV):
        """
        Save the scraped jobs to a CSV file.
        """
        try:
            if self.jobs is not None:
                self.jobs.to_csv(filename, quoting=csv.QUOTE_NONNUMERIC, escapechar="\\", index=False)
                print(f"Jobs saved to {filename}")
            else:
                print("No jobs to save. Please run scrape_jobs first.")

        except Exception as e:
            print("Failed to save jobs to csv - ", e)

    def display_head(self, rows=5):
        """
        Display the first few rows of the scraped jobs.
        """
        try:
            if self.jobs is not None:
                print(self.jobs.head(rows))
            else:
                print("No jobs to display. Please run scrape_jobs first.")

        except Exception as e:
            print("Failed to display jobs")

    def to_json(self, filename=SC.SCRAPED_JOBS_DATA_FILE_JSON):
        """
        Convert the scraped jobs to JSON format and optionally save to a file.
        """
        try:
            if self.jobs is not None:
                jobs_json = self.jobs.to_json(orient="records", indent=4)
                if filename:
                    with open(filename, "w", encoding="utf-8") as json_file:
                        json_file.write(jobs_json)
                    print(f"Jobs saved to {filename} in JSON format")
                return jobs_json
            else:
                print("No jobs to convert. Please run scrape_jobs first.")
                return None

        except Exception as e:
            print("Failed to save jobs to json - ", e)

# Example usage
if __name__ == "__main__":
    scraper = JobScraper(
        site_names=["linkedin", "glassdoor", "google"],
        search_term="Data Scientist",
        google_search_term="Data Scientist",
        job_type="fulltime",
        location="India, Bangalore",
        results_wanted=50,
        hours_old=72,
        linkedin_fetch_description=True
    )
    scraper.scrape_jobs()
    # scraper.display_head()
    scraper.save_to_csv()
    jobs_json = scraper.to_json()
    print(jobs_json)  # Print the JSON representation of the scraped jobs
