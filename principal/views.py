#Python
import datetime
import re

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
            lang="es").items(100)

    final_tweets = [[tweet.id, tweet.full_text, tweet.entities['media'][0]['media_url_https'], tweet.created_at] for tweet in tweets]
    tweet_text = pd.DataFrame(data=final_tweets, columns=['id', 'texto', 'imagen', 'created_at'])
    tweet_text['nombre'] = tweet_text['texto'].apply(lambda x: get_data(x).get('nombre'))
    tweet_text['edad'] = tweet_text['texto'].apply(lambda x: get_data(x).get('edad'))
    tweet_text['fecha'] = tweet_text['texto'].apply(lambda x: get_data(x).get('fecha'))
    tweet_text['ubicacion'] = tweet_text['texto'].apply(lambda x: get_data(x).get('ubicacion'))
    tweet_text['departamento'] = tweet_text['texto'].apply(lambda x: get_data(x).get('departamento'))

    if 'acutal_tweets' in locals():
        acutal_tweets['nombre'] = acutal_tweets['texto'].apply(lambda x: get_data(x).get('nombre'))
        acutal_tweets['edad'] = acutal_tweets['texto'].apply(lambda x: get_data(x).get('edad'))
        acutal_tweets['fecha'] = acutal_tweets['texto'].apply(lambda x: get_data(x).get('fecha'))
        acutal_tweets['ubicacion'] = acutal_tweets['texto'].apply(lambda x: get_data(x).get('ubicacion'))
        acutal_tweets['departamento'] = acutal_tweets['texto'].apply(lambda x: get_data(x).get('departamento'))
        result = tweet_text.append(acutal_tweets)
        print(tweet_text)
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

def get_data(data):
    pattern = r"\s+"
    tweet_text_ = remove_emojis(data.replace('|', '')) # Remover emojis
    tweet_text_array = re.split(pattern, tweet_text_)
    tweet_text_array.pop(0) # Eliminar primer item que contiene AlertaAlbaKenneth
    dict_res = get_variables(tweet_text_array)
    return dict_res

def remove_emojis(data):
    emoji = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002500-\U00002BEF"  # chinese char
        u"\U00002702-\U000027B0"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642"
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
                      "]+", re.UNICODE)
    return re.sub(emoji, '', data)

def get_variables(data):
    nombre = ''
    edad = 'sin edad'
    fecha = ''
    ubicacion = ''
    departamento = ''
    flag_edad = True
    texto = " ".join(data)

    for x in range(len(data)):
        if data[x][-1] == ',':
            nombre += data[x] + ' '
            break
        elif data[x][-1] == '.':
            flag_edad = False
            break
        elif data[x] == 'de' and data[x+1].isdigit():
            break
        nombre += data[x] + ' '

    texto_sin_nombre = texto.replace(nombre, '')

    if flag_edad:
        texto_sin_nombre = texto_sin_nombre.split('.')
        edad = texto_sin_nombre[0]
        texto_sin_nombre.pop(0)
        texto = " ".join(texto_sin_nombre)
    else:
        texto = texto_sin_nombre

    texto = texto.split(',')
    fecha = texto[0]
    texto.pop(0)
    texto = " ".join(texto)
    texto = texto.split('Comparte')
    ubicacion = texto[0]
    lugares = [item for item in ubicacion.split("  ") if item != '']
    departamento = lugares[-1]
    lugares.pop(-1)
    ubicacion = ", ".join(lugares)
    nombre = nombre.replace(",", "")

    dict_res = {
        "nombre": nombre.strip(),
        "edad": edad.strip(),
        "fecha": fecha.strip(),
        "ubicacion": ubicacion.strip(),
        "departamento": departamento.strip(),
    }

    return dict_res

