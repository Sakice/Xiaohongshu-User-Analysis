# This script was generated from the corresponding Jupyter notebook.
# Source notebook: Data_mining.ipynb

# %% [markdown]
# We choose to study content related to "TikTokRefugee" on RedNote and select comments from Reddit as our research subject, aiming to understand changes in people's attitudes toward non-Western social media platforms and potential shifts in migration motivations. We selected "rednote" as the keyword, using the first day of migration as the starting point, and obtained data from the subsequent seven days.

# %% [code]
import os
import praw
import pandas as pd
from datetime import datetime, timezone, timedelta

# Initialize Reddit API client from environment variables.
def initialize_reddit_client():
    client_id = os.getenv("REDDIT_CLIENT_ID")
    client_secret = os.getenv("REDDIT_CLIENT_SECRET")
    user_agent = os.getenv("REDDIT_USER_AGENT")

    missing = [
        name for name, value in {
            "REDDIT_CLIENT_ID": client_id,
            "REDDIT_CLIENT_SECRET": client_secret,
            "REDDIT_USER_AGENT": user_agent,
        }.items()
        if not value
    ]
    if missing:
        raise EnvironmentError(
            "Missing Reddit API environment variables: " + ", ".join(missing)
        )

    return praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent,
    )
# Fetch posts and their comments containing the term 'rednote' from the past week
def fetch_posts_and_comments(term, days=7):
    reddit = initialize_reddit_client()
    subreddit = reddit.subreddit("all")
    
    data = []
    one_week_ago = datetime.now(timezone.utc) - timedelta(days=days)
    for submission in subreddit.search(term, time_filter="week", sort="relevance"):
        post_time = datetime.fromtimestamp(submission.created_utc, timezone.utc)
        if post_time >= one_week_ago:
            # Add post details
            data.append({
                "type": "post",
                "title": submission.title,
                "author": submission.author.name if submission.author else "[deleted]",
                "score": submission.score,
                "url": submission.url,
                "created": post_time,
                "num_comments": submission.num_comments,
                "subreddit": submission.subreddit.display_name,
                "content": submission.selftext
            })

            # Fetch comments
            submission.comments.replace_more(limit=None)
            for comment in submission.comments.list():
                data.append({
                    "type": "comment",
                    "title": submission.title,
                    "author": comment.author.name if comment.author else "[deleted]",
                    "score": comment.score,
                    "url": submission.url,
                    "created": datetime.fromtimestamp(comment.created_utc, timezone.utc),
                    "num_comments": None,
                    "subreddit": submission.subreddit.display_name,
                    "content": comment.body
                })
    return pd.DataFrame(data)

# Save the fetched data to a CSV file
def save_to_csv(dataframe, filename="reddit_data.csv"):
    dataframe.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

if __name__ == "__main__":
    search_term = "rednote"
    data_df = fetch_posts_and_comments(search_term)
    if not data_df.empty:
        save_to_csv(data_df)
    else:
        print(f"No data found for the term '{search_term}' in the past week.")

# %% [code]
import os
import praw
import pandas as pd
from datetime import datetime, timezone, timedelta

# Initialize Reddit API client from environment variables.
def initialize_reddit_client():
    client_id = os.getenv("REDDIT_CLIENT_ID")
    client_secret = os.getenv("REDDIT_CLIENT_SECRET")
    user_agent = os.getenv("REDDIT_USER_AGENT")

    missing = [
        name for name, value in {
            "REDDIT_CLIENT_ID": client_id,
            "REDDIT_CLIENT_SECRET": client_secret,
            "REDDIT_USER_AGENT": user_agent,
        }.items()
        if not value
    ]
    if missing:
        raise EnvironmentError(
            "Missing Reddit API environment variables: " + ", ".join(missing)
        )

    return praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent,
    )
# Fetch posts and comments within the specified time range
def fetch_posts_and_comments(term):
    reddit = initialize_reddit_client()
    subreddit = reddit.subreddit("all")
    
    data = []
    end_time = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)  # Midnight yesterday
    start_time = end_time - timedelta(days=32)  # Midnight 32 days ago
    start_timestamp = start_time.timestamp()
    end_timestamp = end_time.timestamp()
    
    lower_term = term.lower()
    
    for submission in subreddit.search(lower_term, sort="relevance", time_filter="all"):
        post_time = submission.created_utc
        if start_timestamp <= post_time <= end_timestamp:
            # Add post data
            data.append({
                "type": "post",
                "title": submission.title,
                "author": submission.author.name if submission.author else "[deleted]",
                "score": submission.score,
                "url": submission.url,
                "created": datetime.fromtimestamp(post_time, timezone.utc),
                "num_comments": submission.num_comments,
                "subreddit": submission.subreddit.display_name,
                "content": submission.selftext
            })

            # Fetch comments
            submission.comments.replace_more(limit=None)
            for comment in submission.comments.list():
                comment_time = comment.created_utc
                if start_timestamp <= comment_time <= end_timestamp:
                    data.append({
                        "type": "comment",
                        "title": submission.title,
                        "author": comment.author.name if comment.author else "[deleted]",
                        "score": comment.score,
                        "url": submission.url,
                        "created": datetime.fromtimestamp(comment_time, timezone.utc),
                        "num_comments": None,
                        "subreddit": submission.subreddit.display_name,
                        "content": comment.body
                    })
    return pd.DataFrame(data)

# Save data to CSV
def save_to_csv(dataframe, filename="reddit_data_last_32_days.csv"):
    dataframe.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

if __name__ == "__main__":
    search_term = "rednote"
    data_df = fetch_posts_and_comments(search_term)
    if not data_df.empty:
        save_to_csv(data_df)
    else:
        print(f"No data found for '{search_term}' in the past 32 days, ending at midnight yesterday.")

# %% [code]
import os
import praw
import pandas as pd
from datetime import datetime, timezone, timedelta

# Initialize Reddit API client from environment variables.
def initialize_reddit_client():
    client_id = os.getenv("REDDIT_CLIENT_ID")
    client_secret = os.getenv("REDDIT_CLIENT_SECRET")
    user_agent = os.getenv("REDDIT_USER_AGENT")

    missing = [
        name for name, value in {
            "REDDIT_CLIENT_ID": client_id,
            "REDDIT_CLIENT_SECRET": client_secret,
            "REDDIT_USER_AGENT": user_agent,
        }.items()
        if not value
    ]
    if missing:
        raise EnvironmentError(
            "Missing Reddit API environment variables: " + ", ".join(missing)
        )

    return praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent,
    )
import time
from praw.exceptions import APIException, RedditAPIException

# Fetch posts and comments within the specified time range
def fetch_posts_and_comments(term):
    reddit = initialize_reddit_client()
    subreddit = reddit.subreddit("all")
    
    data = []
    end_time = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)  # Midnight yesterday
    start_time = end_time - timedelta(days=32)  # Midnight 32 days ago
    start_timestamp = start_time.timestamp()
    end_timestamp = end_time.timestamp()
    
    lower_term = term.lower()
    
    try:
        for submission in subreddit.search(lower_term, sort="relevance", time_filter="all"):
            time.sleep(2)  # Pause 2 seconds between requests to reduce 429 errors
            post_time = submission.created_utc
            if start_timestamp <= post_time <= end_timestamp:
                # Add post data
                data.append({
                    "type": "post",
                    "title": submission.title,
                    "author": submission.author.name if submission.author else "[deleted]",
                    "score": submission.score,
                    "url": submission.url,
                    "created": datetime.fromtimestamp(post_time, timezone.utc),
                    "num_comments": submission.num_comments,
                    "subreddit": submission.subreddit.display_name,
                    "content": submission.selftext
                })

                # Fetch comments while avoiding too many API requests
                submission.comments.replace_more(limit=0)
                for comment in submission.comments.list():
                    time.sleep(1)  # Reduce request frequency
                    comment_time = comment.created_utc
                    if start_timestamp <= comment_time <= end_timestamp:
                        data.append({
                            "type": "comment",
                            "title": submission.title,
                            "author": comment.author.name if comment.author else "[deleted]",
                            "score": comment.score,
                            "url": submission.url,
                            "created": datetime.fromtimestamp(comment_time, timezone.utc),
                            "num_comments": None,
                            "subreddit": submission.subreddit.display_name,
                            "content": comment.body
                        })
    except (APIException, RedditAPIException) as e:
        print(f"API request failed: {e}")
        print("Pausing for 10 minutes before retrying...")
        time.sleep(600)  # Pause for 10 minutes before retrying after an API 429 rate limit
        return fetch_posts_and_comments(term)  # Retry by calling the function again
    
    return pd.DataFrame(data)

# Save data to CSV
def save_to_csv(dataframe, filename="reddit_data_last_32_days.csv"):
    dataframe.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

if __name__ == "__main__":
    search_term = "rednote"
    data_df = fetch_posts_and_comments(search_term)
    if not data_df.empty:
        save_to_csv(data_df)
    else:
        print(f"No data found for '{search_term}' in the past 32 days, ending at midnight yesterday.")
