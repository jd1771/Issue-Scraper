from github import Github
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
g = Github(github_token)

# List of the repos of interest
frameworks = [
    "facebook/react",
    "angular/angular",
    "vuejs/vue",
    "sveltejs/svelte",
    "emberjs/ember.js",
    "preactjs/preact",
    "jquery/jquery",
    "vercel/next.js",
]

frameworks_to_name = {
    "facebook/react": "React",
    "angular/angular": "Angular",
    "vuejs/vue": "Vue",
    "sveltejs/svelte": "Svelte",
    "emberjs/ember.js": "Ember",
    "preactjs/preact": "Preact",
    "jquery/jquery": "jQuery",
    "vercel/next.js": "Next.js",
}

frameworks_subset = [
    "facebook/react",
]

# Prepare the CSV file
csv_filename = "framework_stats.csv"
csv_header = ["Framework", "Issue ID", "Issue Author", "Closed By", "Labels", "Start Date", "Close Date"]
MAX_ISSUES = 1000

with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(csv_header)

    # Loop through the frameworks list
    for framework in frameworks:
        count = 0
        owner, repo = framework.split("/")
        repo = g.get_repo(framework)

        # Get the closed issues
        issues = repo.get_issues(state="closed")

        for issue in issues:
            if issue.closed_at is not None and issue.created_at is not None:
                if issue.closed_by is None or issue.pull_request:
                    continue  # Skip writing this issue (or pull request)

                count += 1
                start_date = issue.created_at.strftime("%Y-%m-%d %H:%M:%S")
                close_date = issue.closed_at.strftime("%Y-%m-%d %H:%M:%S")
                author = issue.user.login
                closed_by = issue.closed_by.login
                labels = [label.name for label in issue.labels]
                issue_id = issue.number

                # Write the data to the CSV file
                data_row = [frameworks_to_name[framework], issue_id, author, closed_by, labels, start_date, close_date]
                writer.writerow(data_row)
                
                print(f"Done issue {count}")
                
                if count >= MAX_ISSUES:
                    break

                # Check rate limit
                rate_limit = g.get_rate_limit()
                remaining_requests = rate_limit.core.remaining
                reset_time = rate_limit.core.reset.timestamp()

                if remaining_requests <= 25:
                    # Sleep until the rate limit resets
                    sleep_time = reset_time - time.time() + 10  # Add 10 seconds buffer
                    print(f"Reached rate limit. Waiting for {sleep_time} seconds...")
                    time.sleep(sleep_time)

        print(f"Data for {framework} written to CSV file.")

print(f"Data exported to {csv_filename} successfully.")
