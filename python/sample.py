import nltk
from nltk.tag import pos_tag
from nltk.stem.wordnet import WordNetLemmatizer
import re
import string
from nltk import FreqDist
import random
from nltk.tokenize import word_tokenize
import pandas as pd
from nltk.corpus import stopwords
from nltk import classify
import pickle
import requests
import time
import json
from pandas.io.json import json_normalize
import os
stop_words = stopwords.words('english')
from sqlalchemy import create_engine

'''
# For heroku
# '''

# DB = os.environ.get("")
# engine = create_engine(DB)

# '''
# For local
# '''

#database connection
connection_string ="postgres:Shjais2014@localhost:5432/twitter_db"
engine = create_engine(f'postgresql://{connection_string}')


def get_tweets():
    data = pd.read_sql("select * from twitter_tweets;", con=engine)
  
    return data['data'].to_list()


def lemmatize_sentence(tokens):
    lemmatizer = WordNetLemmatizer()
    lemmatized_sentence = []
    for word, tag in pos_tag(tokens):
        if tag.startswith('NN'):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'
        lemmatized_sentence.append(lemmatizer.lemmatize(word, pos))
    return lemmatized_sentence


def remove_noise(tweet_tokens, stop_words=()):

    cleaned_tokens = []

    for token, tag in pos_tag(tweet_tokens):
        token = re.sub(
            'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|'                       '(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', token)
        token = re.sub("(@[A-Za-z0-9_]+)", "", token)

        if tag.startswith("NN"):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'

        lemmatizer = WordNetLemmatizer()
        token = lemmatizer.lemmatize(token, pos)

        if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:
            cleaned_tokens.append(token.lower())
    return cleaned_tokens


def get_all_words(cleaned_tokens_list):
    for tokens in cleaned_tokens_list:
        for token in tokens:
            yield token


def get_our_tweets():
    tweet_list = []
   
    tweets = get_tweets()
    if not tweets:
        print("empty")
    for row in tweets:
        if type(row) is dict:
            tweet_list.append(row['text'])
            

    return tweet_list, 


def clean_our_tweets(tweet_list):
    our_tweet_tokens = []
    our_words = []
    for each in tweet_list:
        our_tweet_tokens.append(nltk.word_tokenize(each))
    clean_tweet_tokens = []
    for each in our_tweet_tokens:
        clean_tweet_tokens.append(remove_noise(each, stop_words))
    return clean_tweet_tokens



def classify_pickle(clean_tweet_tokens):
    loaded_model = pickle.load(open(f"Notebooks/my_classifier.sav", 'rb'))
    print("Loading model")
    tweet = []
    sentiment = []
    for each in clean_tweet_tokens:
        tweet.append(each)
        sentiment.append(loaded_model.classify(
            dict([token, True] for token in each)))
    cleaned_df = pd.DataFrame({"Tokens": tweet, "Emotions": sentiment})
    print(f"Length in script: {len(cleaned_df)}")
    return cleaned_df


print("Cleaning Utility is Ready")
tweet_list, followers = get_our_tweets()
print("Tweets Received")
clean_tweet_tokens = clean_our_tweets(tweet_list)
print("Cleaning Utilized on Tweets")
cleaned_df = classify_pickle(clean_tweet_tokens)
print("Tweets Classified")