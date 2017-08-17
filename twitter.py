import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob


class TwitterClient(object):
    '''
    Generic Twitter Class for the App
    '''
    def __init__(self, query, retweets_only=False, with_sentiment=False):
        # keys and tokens for Twitter
        consumer_key = '3f62IBZwHDcBgjWOBSQsRI1me'
        consumer_secret = 'H0DoIVR51Kg5Vf406ty0CxqdchFkHZXw785rocLfmG5NB8y1U8'
        access_token = '1633140390-703vsmpzWfJY4632q7JzamPdiLyJfIpkzDZUKth'
        access_token_secret = 'sITyF3E10tY8p2g4hBiChqDyMFjqEgJGJ8aSpBdSH5JOl'
        # Attempting authentication
        try:
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            self.auth.set_access_token(access_token, access_token_secret)
            self.query = query
            self.retweets_only = retweets_only
            self.with_sentiment = with_sentiment
            self.api = tweepy.API(self.auth)
            self.tweet_count_max = 100
        except:
            print("Error: Authentication Failed")

    def set_query(self, query=''):
        self.query = query

    def set_retweet_checking(self, retweets_only='false'):
        self.retweets_only = retweets_only

    def set_with_sentiment(self, with_sentiment='false'):
        self.with_sentiment = with_sentiment

    def clean_tweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def get_tweet_sentiment(self, tweet):
        #thresholds to classify pos and neg
        POS_THRESH = 0.2
        NEG_THRESH = 0
        analysis = TextBlob(self.clean_tweet(tweet))
        if analysis.sentiment.polarity > POS_THRESH:
            return 'positive'
        elif analysis.sentiment.polarity < NEG_THRESH:
            return 'negative'
        else:
            return 'neutral'

    def get_tweets(self):
        tweets = []

        try:
            public_tweets = self.api.search(q=self.query, count=self.tweet_count_max,
                                            lang='en')
            if not public_tweets:
                pass
            for tweet in public_tweets:
                parsed_tweet = {}

                parsed_tweet['text'] = tweet.text
                parsed_tweet['user'] = tweet.user.screen_name
                
                if self.with_sentiment == 1:
                    parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)
                else:
                    parsed_tweet['sentiment'] = 'unavailable'

                if tweet.retweet_count > 0 and self.retweets_only == 1:
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                elif not self.retweets_only:
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)

            return tweets

        except tweepy.TweepError as e:
            print("Error : " + str(e))
