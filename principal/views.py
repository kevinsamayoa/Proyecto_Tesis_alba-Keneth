#Python
import datetime
import re

#Django
from django.shortcuts import render

#own
from .utils import get_data

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
        acutal_tweets = acutal_tweets.dropna()
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
            lang="es").items(100)

    final_tweets = [[tweet.id, tweet.full_text, tweet.entities['media'][0]['media_url_https'], tweet.created_at] for tweet in tweets]
    tweet_text = pd.DataFrame(data=final_tweets, columns=['id', 'texto', 'imagen', 'created_at'])
    tweet_text = tweet_text.dropna()
    tweet_text['nombre'] = tweet_text['texto'].apply(lambda x: get_data(x).get('nombre'))
    tweet_text['edad'] = tweet_text['texto'].apply(lambda x: get_data(x).get('edad'))
    tweet_text['fecha'] = tweet_text['texto'].apply(lambda x: get_data(x).get('fecha'))
    tweet_text['ubicacion'] = tweet_text['texto'].apply(lambda x: get_data(x).get('ubicacion'))
    tweet_text['departamento'] = tweet_text['texto'].apply(lambda x: get_data(x).get('departamento'))
    tweet_text['longitud'] = tweet_text['texto'].apply(lambda x: get_data(x).get('longitud'))
    tweet_text['latitud'] = tweet_text['texto'].apply(lambda x: get_data(x).get('latitud'))

    if 'acutal_tweets' in locals():
        acutal_tweets['nombre'] = acutal_tweets['texto'].apply(lambda x: get_data(x).get('nombre'))
        acutal_tweets['edad'] = acutal_tweets['texto'].apply(lambda x: get_data(x).get('edad'))
        acutal_tweets['fecha'] = acutal_tweets['texto'].apply(lambda x: get_data(x).get('fecha'))
        acutal_tweets['ubicacion'] = acutal_tweets['texto'].apply(lambda x: get_data(x).get('ubicacion'))
        acutal_tweets['departamento'] = acutal_tweets['texto'].apply(lambda x: get_data(x).get('departamento'))
        acutal_tweets['longitud'] = acutal_tweets['texto'].apply(lambda x: get_data(x).get('longitud'))
        acutal_tweets['latitud'] = acutal_tweets['texto'].apply(lambda x: get_data(x).get('latitud'))
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

def mapa(request):
    if path_python.exists("tweets.pkl"):
        acutal_tweets = pd.read_pickle("tweets.pkl")
        acutal_tweets = acutal_tweets.dropna()
    else:
        acutal_tweets = pd.DataFrame(data=[], columns=['id', 'texto', 'imagen', 'created_at', 'nombre', 'edad', 'fecha', 'ubicacion', 'departamento', 'longitud', 'latitud'])

    json_records = acutal_tweets.reset_index().to_json(orient ='records', date_format = 'iso')
    data = []
    data = json.loads(json_records)

    context = {
        'data': data
    }
    return render(request, 'mapa.html', context)

