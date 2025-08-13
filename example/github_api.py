from requests import get as reget
from pandas import DataFrame, to_datetime

url = (
    "https://api.github.com/search/repositories?q=language:python&sort=stars&order=desc"
)

result = reget(url).json()

repo_df = DataFrame(result["items"])
repo = repo_df[["full_name", "html_url", "stargazers_count", "watchers"]]
repo["created_year"] = to_datetime(repo_df["created_at"]).dt.year
print(repo.sort_values("stargazers_count").to_markdown())
