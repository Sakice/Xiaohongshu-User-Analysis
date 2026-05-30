# This script was generated from the corresponding Jupyter notebook.
# Source notebook: Coherence Score.ipynb

# %% [markdown]
#  We decided to use LDA language model to analysis the data that we mined from reddit. Before starting the analysis, we need to decide how many topics that we need to analyze. in this case, the coherence score can provide us with a certain level of reference. The code is from: https://medium.com/@kurtsenol21/topic-modeling-lda-mallet-implementation-in-python-part-3-ab03e01b7cd7 

# %% [code]
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
sns.set()

# %% [code]
df = pd.read_csv('reddit_data (1).csv', encoding='utf-8')
df

# %% [code]
import nltk
nltk.download('stopwords')

# %% [code]
import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel
import spacy

# %% [code]
data = list(df.content.astype(str))

# %% [code]
bigram = gensim.models.Phrases(data, min_count=20, threshold=100)
trigram = gensim.models.Phrases(bigram[data], threshold=100)
bigram_mod = gensim.models.phrases.Phraser(bigram)
trigram_mod = gensim.models.phrases.Phraser(trigram)

# %% [code]
# only need tagger, no need for parser and named entity recognizer, for faster implementation
nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])

# get stopwords from nltk library
stop_words = nltk.corpus.stopwords.words('english')

def process_words(texts, stop_words=stop_words, allowed_tags=['NOUN', 'ADJ', 'VERB', 'ADV']):
    
    """Convert a document into a list of lowercase tokens, build bigrams-trigrams, implement lemmatization"""
    
    # remove stopwords, short tokens and letter accents 
    texts = [[word for word in simple_preprocess(str(doc), deacc=True, min_len=3) if word not in stop_words] for doc in texts]
    
    # bi-gram and tri-gram implementation
    texts = [bigram_mod[doc] for doc in texts]
    texts = [trigram_mod[bigram_mod[doc]] for doc in texts]
    
    texts_out = []
    
    # implement lemmatization and filter out unwanted part of speech tags
    for sent in texts:
        doc = nlp(" ".join(sent)) 
        texts_out.append([token.lemma_ for token in doc if token.pos_ in allowed_tags])
    
    # remove stopwords and short tokens again after lemmatization
    texts_out = [[word for word in simple_preprocess(str(doc), deacc=True, min_len=3) if word not in stop_words] for doc in texts_out]    
    
    return texts_out

# %% [code]
data_ready = process_words(data)

# %% [code]
id2word = corpora.Dictionary(data_ready)
print('Total Vocabulary Size:', len(id2word))

# %% [code]
corpus = [id2word.doc2bow(text) for text in data_ready]

# %% [code]
mallet_path = 'mallet-2.0.8/mallet-2.0.8/bin/mallet'

# %% [code]
# display a progress meter
from tqdm import tqdm

def topic_model_coherence_generator(corpus, texts, dictionary, start_topic_count=2, end_topic_count=10, step=1, cpus=1):
  models = []
  coherence_scores = []
  for topic_nums in tqdm(range(start_topic_count, end_topic_count+1, step)):
    mallet_lda_model = gensim.models.wrappers.LdaMallet(mallet_path=mallet_path, corpus=corpus, num_topics=topic_nums,
                                                            id2word=dictionary, iterations=500, workers=cpus)
      
    cv_coherence_model_mallet_lda = gensim. models.CoherenceModel (model=mallet_lda_model, corpus=corpus, texts=texts,
                                                                     dictionary=dictionary, coherence='c_v')
      
    coherence_score = cv_coherence_model_mallet_lda.get_coherence()
    coherence_scores.append(coherence_score)
    models.append(mallet_lda_model)
  return models, coherence_scores

# %% [code]
import multiprocessing
cpus = multiprocessing.cpu_count()  # Use all available CPUs
lda_models, coherence_scores = topic_model_coherence_generator(
    corpus=corpus, texts=data_ready, dictionary=id2word, start_topic_count=2, end_topic_count=50, step=2, cpus=cpus
)

# %% [code]
x_ax = range(2, 2 + len(coherence_scores))  # Adjust x_ax to match y_ax length
y_ax = coherence_scores

plt.figure(figsize=(12, 6))
plt.plot(x_ax, y_ax, c='r')
plt.axvline(x=6, c='k', linestyle='dashed', linewidth=2)
plt.rcParams['figure.facecolor'] = 'white'
plt.xlabel('Number of Topics')
plt.ylabel('Coherence Score')
plt.title('Coherence Score vs. Number of Topics')
plt.show()

# %% [markdown]
# As we can see, the result of coherence score is the highes while the number of topics is six. in this case, we chose 6 topics to analyze the comments through lda model.
