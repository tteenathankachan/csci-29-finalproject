import tweepy as tw
from environs import Env
import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
import itertools
import collections
import os


env = Env()
env.read_env()


consumer_key=os.getenv("consumer_key")
consumer_secret = os.getenv("consumer_secret")
access_token = os.getenv("access_token")
access_token_secret = os.getenv("access_token_secret")
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))


def remove_url_from_text(text):
    """Replace URLs found in a text string with empty strings

    Parameters
    ----------
    txt : string
        String to be parsed.All URL will be removed

    Returns
    -------
    Strings without URLs
    """

    return " ".join(re.sub("([^0-9A-Za-z \t])|(\w+:\/\/\S+)", "", text).split())

def bring_tweets(search_term,api,item_cnt):

    """Calls twitter tweepy cursor  to query based on serach term and return the tweets after removing urls

    Parameters
    ----------
    search_term : string
        String to be parsed.

    api : twitter api

    item_cnt: integer
         Count of tweets to be searched
         Default = 100

    Returns
    -------
    All tweets without URLs
    """

    tweets = tw.Cursor(api.search,
                       q=search_term,
                       lang="en",
                       since='2021-01-01').items(item_cnt)

    all_tweets = [tweet.text for tweet in tweets]
    all_tweets_no_urls = [remove_url_from_text(tweet).lower().split() for tweet in all_tweets]
    return all_tweets_no_urls



def text_transform(all_tweets_no_urls,collection_words):
    """Twitter function for stop word removal, removing collection words ,convert sentences into words and return a list of all words for all searches

    Parameters
    ----------
    all_tweets_no_urls : string
        All tweets from the twitter cursor for the search string

    collection_words : string
        Search string sent that should be removed

    Returns
    -------
    All words without urls
    """
    tweets_nsw = [[word for word in tweet_words if not word in stop_words]
                  for tweet_words in all_tweets_no_urls]
    tweets_nsw_nc = [[w for w in word if not w in collection_words]
                     for word in tweets_nsw]

    # List of all words across tweets
    all_words_no_urls = list(itertools.chain(*tweets_nsw_nc))

    return all_words_no_urls

def tweet_counter(all_words_no_urls):
    """Generate key value pairs for each word as : word : counts
       Parameters
       ----------
       all_words_no_urls : string
           All words without urls

       Returns
       -------
       Word counts
    """

    counts_no_urls = collections.Counter(all_words_no_urls)
    clean_tweets_no_urls = [[k,v]for k, v in counts_no_urls.most_common(10)]
    return clean_tweets_no_urls

def twitter_search(search_string='climatechange',item_cnt=100):
    """Engine that pull the  data from twitter based on the input serach string , performs data wrangling
         and returns the aggregated counts per words
        Parameters
        ----------
        search_string : string
            strings to be searhced
         item_cnt : integer
            number of records to be serached on twitter
            default = 100
        Returns
        -------
        List of Word counts for all tweets for serach text
    """

    auth = tw.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tw.API(auth, wait_on_rate_limit=True)
    search_term = search_string+""+" -filter:retweets"
    all_tweets_no_urls =bring_tweets(search_term,api,item_cnt)
    collection_words = [search_string]
    all_words_no_urls=text_transform(all_tweets_no_urls,collection_words)
    clean_tweets_no_urls = tweet_counter(all_words_no_urls)
    return clean_tweets_no_urls





