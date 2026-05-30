"""Load and sort the raw Reddit dataset by creation timestamp."""

from pathlib import Path

import pandas as pd


INPUT_CSV = Path("data/reddit_data_1.csv")


def load_data(path=INPUT_CSV):
    if not path.exists():
        raise FileNotFoundError(
            "Place reddit_data_1.csv in the data folder, or update INPUT_CSV."
        )
    return pd.read_csv(path, encoding="utf-8")


def sort_by_timestamp(df):
    df = df.copy()
    df["timestamp"] = pd.to_datetime(df["created"])
    return df.sort_values(by="timestamp", ascending=True)


def main():
    df = load_data()
    sorted_df = sort_by_timestamp(df)
    print(sorted_df.head())
    return sorted_df


if __name__ == "__main__":
    main()
