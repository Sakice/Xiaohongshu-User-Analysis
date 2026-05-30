"""Compute LDA-Mallet coherence scores for a range of topic counts."""

import multiprocessing
from pathlib import Path

import gensim
import gensim.corpora as corpora
import matplotlib.pyplot as plt
import nltk
import pandas as pd
import seaborn as sns
import spacy
from gensim.utils import simple_preprocess
from tqdm import tqdm


INPUT_CSV = Path("data/reddit_data (1).csv")
MALLET_PATH = Path("mallet-2.0.8/mallet-2.0.8/bin/mallet")
START_TOPIC_COUNT = 2
END_TOPIC_COUNT = 50
TOPIC_STEP = 2
HIGHLIGHT_TOPIC_COUNT = 6


def load_reddit_content(input_csv=INPUT_CSV):
    df = pd.read_csv(input_csv, encoding="utf-8")
    return list(df.content.astype(str))


def build_phrase_models(data):
    bigram = gensim.models.Phrases(data, min_count=20, threshold=100)
    trigram = gensim.models.Phrases(bigram[data], threshold=100)
    return (
        gensim.models.phrases.Phraser(bigram),
        gensim.models.phrases.Phraser(trigram),
    )


def process_words(texts, bigram_mod, trigram_mod, nlp, stop_words, allowed_tags=None):
    """Tokenize, build n-grams, lemmatize, and remove stopwords."""
    if allowed_tags is None:
        allowed_tags = ["NOUN", "ADJ", "VERB", "ADV"]

    texts = [
        [
            word
            for word in simple_preprocess(str(doc), deacc=True, min_len=3)
            if word not in stop_words
        ]
        for doc in texts
    ]
    texts = [bigram_mod[doc] for doc in texts]
    texts = [trigram_mod[bigram_mod[doc]] for doc in texts]

    texts_out = []
    for sent in texts:
        doc = nlp(" ".join(sent))
        texts_out.append([token.lemma_ for token in doc if token.pos_ in allowed_tags])

    return [
        [
            word
            for word in simple_preprocess(str(doc), deacc=True, min_len=3)
            if word not in stop_words
        ]
        for doc in texts_out
    ]


def prepare_corpus(data):
    nltk.download("stopwords")
    bigram_mod, trigram_mod = build_phrase_models(data)
    nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])
    stop_words = nltk.corpus.stopwords.words("english")
    data_ready = process_words(data, bigram_mod, trigram_mod, nlp, stop_words)
    dictionary = corpora.Dictionary(data_ready)
    print("Total Vocabulary Size:", len(dictionary))
    corpus = [dictionary.doc2bow(text) for text in data_ready]
    return corpus, data_ready, dictionary


def generate_coherence_scores(
    corpus,
    texts,
    dictionary,
    start_topic_count=START_TOPIC_COUNT,
    end_topic_count=END_TOPIC_COUNT,
    step=TOPIC_STEP,
    cpus=1,
):
    models = []
    coherence_scores = []

    for topic_nums in tqdm(range(start_topic_count, end_topic_count + 1, step)):
        model = gensim.models.wrappers.LdaMallet(
            mallet_path=str(MALLET_PATH),
            corpus=corpus,
            num_topics=topic_nums,
            id2word=dictionary,
            iterations=500,
            workers=cpus,
        )
        coherence_model = gensim.models.CoherenceModel(
            model=model,
            corpus=corpus,
            texts=texts,
            dictionary=dictionary,
            coherence="c_v",
        )
        coherence_scores.append(coherence_model.get_coherence())
        models.append(model)

    return models, coherence_scores


def plot_coherence_scores(coherence_scores):
    x_ax = range(START_TOPIC_COUNT, START_TOPIC_COUNT + len(coherence_scores))
    y_ax = coherence_scores

    plt.figure(figsize=(12, 6))
    plt.plot(x_ax, y_ax, c="r")
    plt.axvline(x=HIGHLIGHT_TOPIC_COUNT, c="k", linestyle="dashed", linewidth=2)
    plt.rcParams["figure.facecolor"] = "white"
    plt.xlabel("Number of Topics")
    plt.ylabel("Coherence Score")
    plt.title("Coherence Score vs. Number of Topics")
    plt.show()


def main():
    sns.set()
    data = load_reddit_content()
    corpus, data_ready, dictionary = prepare_corpus(data)
    _, coherence_scores = generate_coherence_scores(
        corpus=corpus,
        texts=data_ready,
        dictionary=dictionary,
        cpus=multiprocessing.cpu_count(),
    )
    plot_coherence_scores(coherence_scores)


if __name__ == "__main__":
    main()
