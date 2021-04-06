

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
output_data_file = "./output_data/tweets.csv"

auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
#auth.set_access_token(access_token, access_token_secret)

seven_days = (dt.datetime.now() - dt.timedelta(days=7)).strftime("%Y-%m-%d")
five_days = (dt.datetime.now() - dt.timedelta(days=5)).strftime("%Y-%m-%d")

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

try:
    api.verify_credentials()
    print("Authentication Complete")
except:
    print("Authentication Unable to Complete")

tweets = []
for tweet in tweepy.Cursor(api.search, q='monday', rpp=100, since=seven_days, until=five_days).items(10):
    tweets.append(tweet)
print(tweets)
    

class TweetAnalyzer():
    def tweets_to_data_frame(self, tweets):
            df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['Tweets'])
    
            df['id'] = np.array([tweet.id for tweet in tweets])
            df['len'] = np.array([len(tweet.text) for tweet in tweets])
            df['date'] = np.array([tweet.created_at for tweet in tweets])
            df['source'] = np.array([tweet.source for tweet in tweets])
            df['likes'] = np.array([tweet.favorite_count for tweet in tweets])
            df['retweets'] = np.array([tweet.retweet_count for tweet in tweets])
    
            return df

if __name__ == '__main__':

    tweet_analyzer = TweetAnalyzer()
    df = tweet_analyzer.tweets_to_data_frame(tweets)
    print(df.head(10))


#Write DataFrame to CSV file "cities.csv"
df.to_csv(output_data_file)
#status = api.get_status(id, tweet_mode="extended")
#try:
#    print(status.retweeted_status.full_text)
#except AttributeError:  # Not a Retweet
#    print(status.full_text)

#for status in tweepy.Cursor(api.user_timeline).items():
#    # process status here
#    process_status(status)
#    
#def on_status(self, status):
#    if hasattr(status, "retweeted_status"):  # Check if Retweet
#        try:
#            print(status.retweeted_status.extended_tweet["full_text"])
#        except AttributeError:
#            print(status.retweeted_status.text)
#    else:
#        try:
#            print(status.extended_tweet["full_text"])
#        except AttributeError:
#            print(status.text)
            
            

#for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
#    tweets.append(tweet)
#return tweets