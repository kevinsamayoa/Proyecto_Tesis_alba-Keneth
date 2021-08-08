#Python
import datetime

#Django
from django.shortcuts import render

#3rd
import json
import tweepy
import pandas as pd
import os.path
from os import path as path_python

def home(request):
    consumer_key = "2lfFxUOsxNjLPMWiaWeP8kpk6"
    consumer_secret = "qIPsGoHVfolDk6qjbVEvhEa5opXYQD6xM4lMxWmT4YOC0A7Cem"
    access_token = "1245440519519567876-jxHGeo5ybqSTwxDDjUF7WK4BTRGXgW"
    access_token_secret = "Fr3q3lfKHMF2sFh2nmJRf66qyr57Y2xpReYezytpwHiCy"

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)

    # public_tweets = api.home_timeline(1)

    today = datetime.date.today()
    yesterday= today - datetime.timedelta(days=1)

    if path_python.exists("tweets.pkl"):
        acutal_tweets = pd.read_pickle("tweets.pkl")
        last_id = acutal_tweets.iloc[0][['id']].values[0]

        tweets = tweepy.Cursor(
            api.search,
            q="from:alba_keneth #AlertaAlbaKeneth -filter:retweets",
            tweet_mode='extended',
            lang="es",
            since_id=last_id).items()

    else:
        tweets = tweepy.Cursor(
            api.search,
            q="from:alba_keneth #AlertaAlbaKeneth -filter:retweets",
            tweet_mode='extended',
            lang="es").items()

    final_tweets = [[tweet.id, tweet.full_text, tweet.entities['media'][0]['media_url_https'], tweet.created_at] for tweet in tweets]
    tweet_text = pd.DataFrame(data=final_tweets, columns=['id', 'texto', 'imagen', 'created_at'])

    if 'acutal_tweets' in locals():
        result = tweet_text.append(acutal_tweets)
        result.to_pickle("tweets.pkl")
        json_records = result.reset_index().to_json(orient ='records', date_format = 'iso')
    else:
        tweet_text.to_pickle("tweets.pkl")
        json_records = tweet_text.reset_index().to_json(orient ='records', date_format = 'iso')

    data = []
    data = json.loads(json_records)

    context = {
        'data': data
    }

    return render(request, 'index.html', context)
