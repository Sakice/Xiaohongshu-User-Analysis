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
# 爬取特定时间段内的帖子和评论
def fetch_posts_and_comments(term):
    reddit = initialize_reddit_client()
    subreddit = reddit.subreddit("all")
    
    data = []
    end_time = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)  # 昨天午夜
    start_time = end_time - timedelta(days=32)  # 32天前的午夜
    start_timestamp = start_time.timestamp()
    end_timestamp = end_time.timestamp()
    
    lower_term = term.lower()
    
    for submission in subreddit.search(lower_term, sort="relevance", time_filter="all"):
        post_time = submission.created_utc
        if start_timestamp <= post_time <= end_timestamp:
            # 添加帖子数据
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

            # 获取评论
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

# 保存数据到 CSV
def save_to_csv(dataframe, filename="reddit_data_last_32_days.csv"):
    dataframe.to_csv(filename, index=False)
    print(f"数据已保存至 {filename}")

if __name__ == "__main__":
    search_term = "rednote"
    data_df = fetch_posts_and_comments(search_term)
    if not data_df.empty:
        save_to_csv(data_df)
    else:
        print(f"在过去 32 天（截至昨日午夜）期间，没有找到与 '{search_term}' 相关的数据。")

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

# 爬取特定时间段内的帖子和评论
def fetch_posts_and_comments(term):
    reddit = initialize_reddit_client()
    subreddit = reddit.subreddit("all")
    
    data = []
    end_time = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)  # 昨天午夜
    start_time = end_time - timedelta(days=32)  # 32天前的午夜
    start_timestamp = start_time.timestamp()
    end_timestamp = end_time.timestamp()
    
    lower_term = term.lower()
    
    try:
        for submission in subreddit.search(lower_term, sort="relevance", time_filter="all"):
            time.sleep(2)  # 每个请求之间暂停 2 秒，减少 429 发生率
            post_time = submission.created_utc
            if start_timestamp <= post_time <= end_timestamp:
                # 添加帖子数据
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

                # 获取评论，避免过多 API 请求
                submission.comments.replace_more(limit=0)
                for comment in submission.comments.list():
                    time.sleep(1)  # 降低请求频率
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
        print(f"API 请求失败: {e}")
        print("暂停 10 分钟后重试...")
        time.sleep(600)  # 遇到 API 429 限制时，暂停 10 分钟再试
        return fetch_posts_and_comments(term)  # 递归调用，尝试重新抓取
    
    return pd.DataFrame(data)

# 保存数据到 CSV
def save_to_csv(dataframe, filename="reddit_data_last_32_days.csv"):
    dataframe.to_csv(filename, index=False)
    print(f"数据已保存至 {filename}")

if __name__ == "__main__":
    search_term = "rednote"
    data_df = fetch_posts_and_comments(search_term)
    if not data_df.empty:
        save_to_csv(data_df)
    else:
        print(f"在过去 32 天（截至昨日午夜）期间，没有找到与 '{search_term}' 相关的数据。")
