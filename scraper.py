from github import Github
from github import Auth
from datetime import datetime
from dotenv import load_dotenv
import os
import csv
import time

# Load environment variables from .env file
load_dotenv()

# Access the GitHub token
github_token = os.getenv("GITHUB_TOKEN")

# using an access token
auth = Auth.Token(github_token)

# Enter your GitHub personal access token here
g = Github(auth=auth)

# List of the repos of interest
frameworks = [
    "facebook/react",
    "angular/angular",
    "vuejs/vue",
    "sveltejs/svelte",
    "emberjs/ember.js",
    "preactjs/preact",
    "polymer/polymer",
    "jashkenas/backbone",
    "knockout/knockout",
    "MithrilJS/mithril.js"
]

## Subset of the repos of interest (for testing purposes)
frameworks_subset = [
    "facebook/react",
    "angular/angular",
    "vuejs/vue",
]

# Prepare the CSV file
csv_filename = "framework_stats.csv"
csv_header = ["Framework", "Contributors", "Commits", "Issue Resolution Time (s)"]

with open(csv_filename, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(csv_header)

    # Loop through the frameworks list
    for framework in frameworks_subset:
        owner, repo = framework.split("/")
        repo = g.get_repo(framework)

        # Get the number of contributors
        contributors = repo.get_contributors().totalCount

        # Get the number of commits
        commits = repo.get_commits().totalCount

        # Get the average issue resolution time
        issues = repo.get_issues(state="closed")[:50]
        total_resolution_time = 0
        total_resolved_issues = 0


        count = 0
        cumulative_time_to_close = 0
        for issue in issues:
            if issue.closed_at is not None and issue.created_at is not None:
                count += 1
                time_to_close = issue.closed_at - issue.created_at
                cumulative_time_to_close += time_to_close.total_seconds()

        avg_resolution_time = cumulative_time_to_close / count

        # Write the data to the CSV file
        data_row = [framework, contributors, commits, avg_resolution_time]
        writer.writerow(data_row)

        print(f"Data for {framework} written to CSV file.")

        # Delay for a few seconds to avoid hitting the rate limits
        time.sleep(2)


print(f"Data exported to {csv_filename} successfully.")
