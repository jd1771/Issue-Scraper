from github import Github
from datetime import datetime

# Enter your GitHub personal access token here
g = Github("your_access_token")

# Specify the repository
repo = g.get_repo("facebook/react")

closed_issues = repo.get_issues(state='closed')[:50]

count = 0
avg_time_to_close = 0
for issue in closed_issues:
    if issue.closed_at is not None and issue.created_at is not None:
        count += 1
        time_to_close = issue.closed_at - issue.created_at
        avg_time_to_close += time_to_close.total_seconds()
        print(f"Issue {issue.number} was closed in {time_to_close.total_seconds()} seconds")
print(f"Average time to close: {avg_time_to_close / count} seconds")