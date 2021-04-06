from nltk.tokenize import word_tokenize
# from nlp_sentiment_words import text, cleaned_tokens, df
import pandas as pd
from bs4 import BeautifulSoup
import urllib.request

# Output File (CSV)
output_data_file = "../output_data/sentiment.csv"

# scrape the data(tweets) from the the S3 bucket after it's called in
response =  urllib.request.urlopen('https://data-bootcamp-036.s3.us-east-2.amazonaws.com/friday_tweets.csv')
html = response.read()
# print(html)

# pull data out of the html response and strip all html tags
soup = BeautifulSoup(html,'html5lib')
text = soup.get_text(strip = True)

# print(text)

# tokenize the data (split into separate words)
from nltk.tokenize import TweetTokenizer
tokened = TweetTokenizer()
tokens = tokened.tokenize(text)

def tokenize_this_list(text):
    token_list = []
    token_count = []
    for each in text:
        tokens = word_tokenize(each)
        count = len(tokens)
        token_list.append(tokens)
        token_count.append(count)
    # return token_count, token_list
    print(token_count, token_list)

# NRC
def create_nrc():
    filepath = "../NRC-Sentiment-Emotion-Lexicons/NRC-Emotion-Lexicon-v0.92/NRC-Emotion-Lexicon-Wordlevel-v0.92.txt"
    emolex_df = pd.read_csv(filepath,  names=["word", "emotion", "association"], skiprows=45, sep='\t')
    emolex_words = emolex_df.pivot(index='word', columns='emotion', values='association').reset_index()
    return emolex_words


def full_list(text, df):
    token_count, token_list = tokenize_this_list(text)
    # Set list to hold dictionary and return
    emo_list = []
    # Loop through tweets in list
    for tweet in token_list:
        # Set dictionary to hold emotions as keys and their counts as values
        lexi_dict = {}
        # Loop through words in tweet
        for word in tweet:
            # Check if word is in df -> emotion lexicon dataframe (emolex_df) in our example
            if word in df.word.to_list():
                # List to hold index where association column is 1
                assoc = []
                # Get indices where word from tweet is in df
                i = df.index[df['word'] == word]
                for index in i:
                    # Check if association is 1 (not 0) and append to list
                    if df['association'].iloc[index] == 1:
                        assoc.append(index)
                    # Where the word from tweet has association = 1, add to dict if not there, or update count if there
                    for j in assoc:
                        emo = df['emotion'].iloc[j]
                        if (emo in lexi_dict.keys()):
                            lexi_dict[emo] += 1
                        else:
                            lexi_dict[emo] = 1
        # Append to list
        emo_list.append(lexi_dict)
    # return list
    return emo_list



# emolex_df = create_nrc()
# print(emolex_df)
# emolex_df.to_csv(output_data_file)