"""Collect Reddit posts and comments for the RedNote/TikTokRefugee dataset."""

import os
import time
from datetime import datetime, timedelta, timezone

import pandas as pd
import praw
from praw.exceptions import APIException, RedditAPIException


SEARCH_TERM = "rednote"
OUTPUT_CSV = "reddit_data_last_32_days.csv"
DEFAULT_DAYS = 32
REQUEST_PAUSE_SECONDS = 2
COMMENT_PAUSE_SECONDS = 1
RATE_LIMIT_PAUSE_SECONDS = 600


def initialize_reddit_client():
    """Initialize the Reddit API client from environment variables."""
    client_id = os.getenv("REDDIT_CLIENT_ID")
    client_secret = os.getenv("REDDIT_CLIENT_SECRET")
    user_agent = os.getenv("REDDIT_USER_AGENT")

    missing = [
        name
        for name, value in {
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


def _record_submission(submission, created_at):
    return {
        "type": "post",
        "title": submission.title,
        "author": submission.author.name if submission.author else "[deleted]",
        "score": submission.score,
        "url": submission.url,
        "created": created_at,
        "num_comments": submission.num_comments,
        "subreddit": submission.subreddit.display_name,
        "content": submission.selftext,
    }


def _record_comment(submission, comment, created_at):
    return {
        "type": "comment",
        "title": submission.title,
        "author": comment.author.name if comment.author else "[deleted]",
        "score": comment.score,
        "url": submission.url,
        "created": created_at,
        "num_comments": None,
        "subreddit": submission.subreddit.display_name,
        "content": comment.body,
    }


def fetch_posts_and_comments(term, days=DEFAULT_DAYS):
    """Fetch posts and comments in the target time window."""
    reddit = initialize_reddit_client()
    subreddit = reddit.subreddit("all")

    data = []
    end_time = datetime.now(timezone.utc).replace(
        hour=0, minute=0, second=0, microsecond=0
    )
    start_time = end_time - timedelta(days=days)
    start_timestamp = start_time.timestamp()
    end_timestamp = end_time.timestamp()

    try:
        for submission in subreddit.search(term.lower(), sort="relevance", time_filter="all"):
            time.sleep(REQUEST_PAUSE_SECONDS)
            post_time = submission.created_utc
            if not start_timestamp <= post_time <= end_timestamp:
                continue

            data.append(
                _record_submission(
                    submission,
                    datetime.fromtimestamp(post_time, timezone.utc),
                )
            )

            submission.comments.replace_more(limit=0)
            for comment in submission.comments.list():
                time.sleep(COMMENT_PAUSE_SECONDS)
                comment_time = comment.created_utc
                if start_timestamp <= comment_time <= end_timestamp:
                    data.append(
                        _record_comment(
                            submission,
                            comment,
                            datetime.fromtimestamp(comment_time, timezone.utc),
                        )
                    )
    except (APIException, RedditAPIException) as error:
        print(f"API request failed: {error}")
        print("Pausing for 10 minutes before retrying...")
        time.sleep(RATE_LIMIT_PAUSE_SECONDS)
        return fetch_posts_and_comments(term, days=days)

    return pd.DataFrame(data)


def save_to_csv(dataframe, filename=OUTPUT_CSV):
    dataframe.to_csv(filename, index=False)
    print(f"Data saved to {filename}")


def main():
    data_df = fetch_posts_and_comments(SEARCH_TERM)
    if not data_df.empty:
        save_to_csv(data_df)
    else:
        print(
            f"No data found for '{SEARCH_TERM}' in the past {DEFAULT_DAYS} days, "
            "ending at midnight yesterday."
        )


if __name__ == "__main__":
    main()
