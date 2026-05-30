# This script was generated from the corresponding Jupyter notebook.
# Source notebook: df.ipynb

# %% [code]
import pandas as pd
from pathlib import Path

# Keep data paths relative so the notebook works after cloning the repository.
df_path = Path("reddit_data_1.csv")
if not df_path.exists():
    raise FileNotFoundError(
        "Place reddit_data_1.csv in the project root, or update df_path to another relative path."
    )

df = pd.read_csv(df_path, encoding="utf-8")

df

# %% [code]
df["timestamp"] = pd.to_datetime(df["created"])
df = df.sort_values(by="timestamp", ascending=True)
df
