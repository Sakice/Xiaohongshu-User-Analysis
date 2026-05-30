# This script was generated from the corresponding Jupyter notebook.
# Source notebook: Topic_Modeling_LDA_Mallet.ipynb

# %% [markdown]
# The code is from: https://medium.com/@kurtsenol21/topic-modeling-lda-mallet-implementation-in-python-part-3-ab03e01b7cd7 
# We edit a bit and add clean data code before training the LDA model.

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
df.info()

# %% [code]
import pandas as pd
import re

# Load data
def load_data(file_path):
    return pd.read_csv(file_path)

# Clean data
def clean_text(text):
    # Remove URLs, low-information words, and special characters
    text = re.sub(r"http\S+|www\S+", "", text)  # Remove URLs
    text = re.sub(r"[^a-zA-Z\s]", "", text)    # Remove non-letter characters
    text = re.sub(r"\b\w{1,2}\b", "", text)    # Remove 1-2 character words
    text = text.lower()                        # Convert to lowercase
    return text.strip()

def clean_data(df, column_name):
    df[column_name] = df[column_name].fillna("").apply(clean_text)
    return df

# Main function
def main(input_file, output_csv):
    # Load data
    df = load_data(input_file)

    # Clean data
    df = clean_data(df, 'content')

    # Save cleaned and analyzed data
    df.to_csv(output_csv, index=False)
    print(f"Cleaned data saved to {output_csv}")


# Run script
if __name__ == "__main__":
    input_csv = "reddit_data (1).csv"  # Input CSV file path
    output_csv = "reddit_clean_data"  # Output CSV file path
    main(input_csv, output_csv)

# %% [code]
df = df = pd.read_csv('reddit_clean_data', encoding='utf-8')
df

# %% [code]
import nltk
nltk.download('stopwords')

# %% [code]
import pyLDAvis
import pyLDAvis.gensim

# %% [code]
import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel

# %% [code]
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
data_ready

# %% [code]
id2word = corpora.Dictionary(data_ready)
print('Total Vocabulary Size:', len(id2word))

# %% [code]
corpus = [id2word.doc2bow(text) for text in data_ready]

# %% [code]
dict_corpus = {}

for i in range(len(corpus)):
  for idx, freq in corpus[i]:
    if id2word[idx] in dict_corpus:
      dict_corpus[id2word[idx]] += freq
    else:
       dict_corpus[id2word[idx]] = freq
       
dict_df = pd.DataFrame.from_dict(dict_corpus, orient='index', columns=['freq'])

# %% [code]
plt.figure(figsize=(8,6))
sns.distplot(dict_df['freq'], bins=100);

# %% [code]
dict_df.sort_values('freq', ascending=False).head(10)

# %% [code]
extension = dict_df[dict_df.freq>1000].index.tolist()

# %% [code]
ids=[id2word.token2id[extension[i]] for i in range(len(extension))]
id2word.filter_tokens(bad_ids=ids)

# %% [code]
# add high frequency words to stop words list
stop_words.extend(extension)
# rerun the process_words function
data_ready = process_words(data)
# recreate Dictionary
id2word = corpora.Dictionary(data_ready)
print('Total Vocabulary Size:', len(id2word))

# %% [code]
# Filter out words that occur less than 10 documents, or more than
# 50% of the documents.
id2word.filter_extremes(no_below=10, no_above=0.5)
print('Total Vocabulary Size:', len(id2word))

# %% [code]
# Create Corpus: Term Document Frequency
corpus = [id2word.doc2bow(text) for text in data_ready]

# %% [code]
mallet_path = 'mallet-2.0.8/mallet-2.0.8/bin/mallet'

# %% [code]
ldamallet = gensim.models.wrappers.LdaMallet(mallet_path, corpus=corpus, num_topics=6, id2word=id2word)

# %% [code]
from pprint import pprint
# display topics
pprint(ldamallet.show_topics(formatted=False))

# %% [code]
# Compute Coherence Score
coherence_model_ldamallet = CoherenceModel(model=ldamallet, texts=data_ready, dictionary=id2word, coherence='c_v')
coherence_ldamallet = coherence_model_ldamallet.get_coherence()
print('Coherence Score: ', coherence_ldamallet)

# %% [markdown]
# Save lda model

# %% [code]
import pickle
pickle.dump(ldamallet, open("PKL/ldamallet.pkl", "wb"))

# %% [code]
ldamallet.save("PKL/lda_model")

# %% [markdown]
# Save lda model dictionary

# %% [code]
dictionary = ldamallet.id2word
dictionary_path = "PKL/dictionary.dict"
dictionary.save(dictionary_path)
print(f"Dictionary saved to {dictionary_path}")

# %% [code]
tm_results = ldamallet[corpus]

# %% [code]
corpus_topics = [sorted(topics, key=lambda record: -record[1])[0] for topics in tm_results]

# %% [code]
topics = [[(term, round(wt, 3)) for term, wt in ldamallet.show_topic(n, topn=6)] for n in range(0, ldamallet.num_topics)]

# %% [code]
topics_df = pd.DataFrame([[term for term, wt in topic] for topic in topics], columns = ['Term'+str(i) for i in range(1, 7)], index=['Topic '+str(t) for t in range(1, ldamallet.num_topics+1)]).T
topics_df.head()

# %% [code]
# set column width
pd.set_option('display.max_colwidth', None)

# Create the DataFrame
topics_df = pd.DataFrame(
    [', '.join([term for term, wt in topic]) for topic in topics],
    columns=['Terms per Topic'],
    index=['Topic' + str(t) for t in range(1, ldamallet.num_topics + 1)]
)

# Display the DataFrame
topics_df

# %% [code]
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Initialize the WordCloud object
wc = WordCloud(background_color="white", colormap="Dark2", max_font_size=150, random_state=42)

# Set figure size
plt.rcParams['figure.figsize'] = [20, 15]

# Set the subplot layout dynamically
rows = 2  # Number of rows
cols = 3  # Number of columns

# Generate word clouds for each topic
for i in range(min(len(topics_df), rows * cols)):  # Ensure the topic count is not exceeded
    wc.generate(text=topics_df["Terms per Topic"][i])
    
    plt.subplot(rows, cols, i + 1)
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.title(f"Topic {topics_df.index[i]}")

# Show the figure
plt.tight_layout()
plt.show()

# Save the word cloud figure
plt.savefig("wordcloud_topics.png", dpi=300, bbox_inches="tight")

# %% [code]
from gensim.models.ldamodel import LdaModel

def convertldaMalletToldaGen(mallet_model):
    model_gensim = LdaModel(
        id2word=mallet_model.id2word, num_topics=mallet_model.num_topics,
        alpha=mallet_model.alpha) 
    model_gensim.state.sstats[...] = mallet_model.wordtopics
    model_gensim.sync_state()
    return model_gensim

# %% [code]
ldagensim = convertldaMalletToldaGen(ldamallet)

# %% [code]
import pyLDAvis.gensim as gensimvis
vis_data = gensimvis.prepare(ldagensim, corpus, id2word, sort_topics=False)
pyLDAvis.display(vis_data)

# %% [code]
import pyLDAvis.gensim as gensimvis
import pyLDAvis

# Prepare visualization data
vis_data = gensimvis.prepare(ldagensim, corpus, id2word, sort_topics=False)

# Display visualization results
pyLDAvis.display(vis_data)

# Save visualization results as an HTML file
pyLDAvis.save_html(vis_data, 'lda_visualization.html')

# %% [code]
df

# %% [code]
# create a dataframe
corpus_topic_df = pd.DataFrame()
# get the Titles from the original dataframe
# corpus_topic_df['Title'] = df['title']
corpus_topic_df['Dominant Topic'] = [item[0]+1 for item in corpus_topics]
corpus_topic_df['Contribution %'] = [round(item[1]*100, 2) for item in corpus_topics]
corpus_topic_df['Topic Terms'] = [topics_df.iloc[t[0]]['Terms per Topic'] for t in corpus_topics]
corpus_topic_df.head()

# %% [code]
dominant_topic_df = corpus_topic_df.groupby('Dominant Topic').agg(
                                  Doc_Count = ('Dominant Topic', np.size),
                                  Total_Docs_Perc = ('Dominant Topic', np.size)).reset_index()

dominant_topic_df['Total_Docs_Perc'] = dominant_topic_df['Total_Docs_Perc'].apply(lambda row: round((row*100) / len(corpus), 2))

dominant_topic_df

# %% [code]
corpus_topic_df.groupby('Dominant Topic').apply(lambda topic_set: (topic_set.sort_values(by=['Contribution %'], ascending=False).iloc[0])).reset_index(drop=True)

# %% [code]
pprint(tm_results[0])

# %% [code]
df_weights = pd.DataFrame.from_records([{v: k for v, k in row} for row in tm_results])
df_weights.columns = ['Topic ' + str(i) for i in range(1,7)]
df_weights

# %% [code]
df['created'] = pd.to_datetime(df['created'])
df['date'] = df['created'].dt.date

df_weights['Date'] = df['date']

df_weights.groupby('Date').mean()

# %% [code]
df_weights['Dominant'] = df_weights.drop('Date', axis=1).idxmax(axis=1)
df_weights.head()

# %% [code]
df_dominance = df_weights.groupby('Date')['Dominant'].value_counts(normalize=True).unstack()
df_dominance
