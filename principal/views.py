#Python
import datetime
import re

#Django
from django.shortcuts import render

#own
from .utils import get_data
from .models import *

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
    alertas = Alertas.objects.all()

    if alertas.count() > 0:
        last_id = alertas.order_by('-tweet_id').first().tweet_id
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
            lang="es").items(200)

    final_tweets = []
    for tweet in tweets:
        if 'media' in tweet.entities:
            final_tweets.append([tweet.id, tweet.full_text, tweet.entities['media'][0]['media_url_https'], tweet.created_at])

    tweet_text = pd.DataFrame(data=final_tweets, columns=['id', 'texto', 'imagen', 'created_at'])
    # Obtener los datos importantes del texto
    tweet_text['nombre'] = tweet_text['texto'].apply(lambda x: get_data(x).get('nombre'))
    tweet_text['edad'] = tweet_text['texto'].apply(lambda x: get_data(x).get('edad'))
    tweet_text['fecha'] = tweet_text['texto'].apply(lambda x: get_data(x).get('fecha'))
    tweet_text['ubicacion'] = tweet_text['texto'].apply(lambda x: get_data(x).get('ubicacion'))
    tweet_text['departamento'] = tweet_text['texto'].apply(lambda x: get_data(x).get('departamento'))
    tweet_text['longitud'] = tweet_text['texto'].apply(lambda x: get_data(x).get('longitud'))
    tweet_text['latitud'] = tweet_text['texto'].apply(lambda x: get_data(x).get('latitud'))
    tweet_text['texto'] = tweet_text['texto'].apply(lambda x: get_data(x).get('texto'))
    tweet_text = tweet_text.dropna()

    for index, row in tweet_text.iterrows():
        try:
            a = Alertas(
                tweet_id = row['id'],
                texto_tweet = row['texto'],
                nombre = row['nombre'],
                edad = row['edad'],
                ubicacion = row['ubicacion'],
                fecha = row['fecha'],
                departamento = row['departamento'],
                longitud = row['longitud'],
                latitud = row['latitud'],
                imagen_link = row['imagen'],
                created_at = row['created_at']
            )
            a.save()
        except Exception as e:
            print(e)

    context = {
        'data': alertas
    }

    return render(request, 'index.html', context)

def mapa(request):
    alertas = Alertas.objects.all()

    context = {
        'data': alertas
    }
    return render(request, 'mapa.html', context)

def dashboard(request):
    alertas = Alertas.objects.all()
    acutal_tweets = pd.DataFrame(list(alertas.values('tweet_id', 'texto_tweet', 'imagen_link', 'created_at', 'nombre', 'edad', 'fecha', 'ubicacion', 'departamento', 'longitud', 'latitud')))
    top_cinco = acutal_tweets.groupby(by=["departamento"]).count()['tweet_id'].sort_values(ascending=False).head(5)
    top_cinco_pais = top_cinco.index.tolist()
    top_cinco_count = top_cinco.values.tolist()
    top_cincos_edad = acutal_tweets.groupby(by=["edad"]).count()['tweet_id'].sort_values(ascending=False).head(5)
    top_cinco_edad = top_cincos_edad.index.tolist()
    top_cinco_edad = [float(x) for x in top_cinco_edad]
    top_cinco_edad_count = top_cincos_edad.values.tolist()

    context = {
        'top_cinco_pais': top_cinco_pais,
        'top_cinco_count': top_cinco_count,
        'top_cinco_edad': top_cinco_edad,
        'top_cinco_edad_count': top_cinco_edad_count,
    }
    return render(request, 'dashboard.html', context)

def manual(request):
    return render(request, 'manual.html')
