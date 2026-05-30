# TikTokRefugee / RedNote Reddit Analysis

This repository contains the data, analysis code, models, figures, and HTML outputs for a group project in the Data Project course of the Cultural Data & AI master's program at the University of Amsterdam.

Authors: Jiayi Zhu, Bowen Zhang, Xinyi Hu, Ahmet S. Sakrak, and Xinran Zhang.

The project studies Reddit discussion related to TikTokRefugee and RedNote during the 2025 TikTok ban period, with a focus on attitudes toward non-Western social media platforms and possible changes in migration motivations.

## Repository Structure

- `data/`: raw Reddit CSV data.
- `analysis-code/`: Python analysis scripts.
- `outputs/`: generated cleaned data, models, figures, topic files, network analyses, and HTML outputs.
- `mallet-2.0.8/`: local MALLET dependency used by the LDA-Mallet model.

## Data

- Raw data is stored in `data/`.
- Cleaned data is stored in `outputs/reddit_clean_data`.
- Generated topic-level CSV files are stored in `outputs/topic_csv_file/`.

## Analysis Code

The analysis code is stored as Python scripts in `analysis-code/`:

- `Step_1_Data_mining.py`
- `Step_2_df.py`
- `Step_3_Coherence_Score.py`
- `Step_4_graphs.py`
- `Step_5_Topic_Modeling_LDA_Mallet.py`
- `Step_6_HTML.py`

## Setup Before Data Collection

Do not commit real Reddit API credentials to GitHub.

Create a local `.env` file from `.env.example`, then fill in:

- `REDDIT_CLIENT_ID`
- `REDDIT_CLIENT_SECRET`
- `REDDIT_USER_AGENT`

Load these values as environment variables before running `analysis-code/Step_1_Data_mining.py`.

Data files should use repository-relative paths, for example `data/reddit_data_1.csv`. If your data is stored elsewhere, update the script path to another relative path.

## Outputs

Generated results are stored in `outputs/`, including:

- `outputs/PKL/`: trained LDA-Mallet model files and dictionary.
- `outputs/lda_visualization.html`: interactive LDA visualization.
- `outputs/wordcloud_topics.png`: topic word-cloud figure.
- `outputs/topic_frequency_over_time.png`: topic frequency over time.
- `outputs/horizon_graph_topic_count_over_time.png`: horizon graph of topic counts.
- `outputs/terms_cluster_per_topic/`: topic network analyses and visualizations.

## Notes

- Rerunning `analysis-code/Step_5_Topic_Modeling_LDA_Mallet.py` will retrain the LDA model and may produce different topic assignments or figures.
- If retraining the LDA model, check the MALLET path in the script. The local MALLET executable is expected under `mallet-2.0.8/mallet-2.0.8/bin/mallet`.
- `outputs/PKL/dictionary.dict` is the vocabulary dictionary generated during model training.
- `outputs/PKL/lda_model` is the LDA-Mallet model used in this analysis.
- `outputs/PKL/ldamallet.pkl` is a pickled version of the trained LDA-Mallet model.
