# pip install tweepy
from config import consumer_key,consumer_secret,access_token,access_token_secret
import tweepy
from tweepy import API 
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import datetime as dt
import numpy as np
import pandas as pd

# Output File (CSV)
output_data_file = "./output_data/april_tweets.csv"

auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
#auth.set_access_token(access_token, access_token_secret)

#03/28/2021
date_since = (dt.datetime(2021, 3, 31)).strftime("%Y-%m-%d")
#03/30/2021
date_until = (dt.datetime(2021, 4, 2)).strftime("%Y-%m-%d")

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

try:
    api.verify_credentials()
    print("Authentication Complete")
except:
    print("Authentication Unable to Complete")

tweets = []
for tweet in tweepy.Cursor(api.search, q='april', lang='en', rpp=100, since=date_since, until=date_until).items(450):
    tweets.append(tweet)
print(tweets)
    

class TweetAnalyzer():
    def tweets_to_data_frame(self, tweets):
            df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['Tweets'])
    
            # df['id'] = np.array([tweet.id for tweet in tweets])
            # df['len'] = np.array([len(tweet.text) for tweet in tweets])
            # df['date'] = np.array([tweet.created_at for tweet in tweets])
            # df['source'] = np.array([tweet.source for tweet in tweets])
            # df['likes'] = np.array([tweet.favorite_count for tweet in tweets])
            # df['retweets'] = np.array([tweet.retweet_count for tweet in tweets])
    
            return df

if __name__ == '__main__':

    tweet_analyzer = TweetAnalyzer()
    df = tweet_analyzer.tweets_to_data_frame(tweets)
    print(df.head(10))


#Write DataFrame to CSV file "cities.csv"
df.to_csv(output_data_file)