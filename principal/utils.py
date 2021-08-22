#Python
import datetime
import re
import random

#Own
from .data import get_coordenadas

#3rd
import json
import tweepy
import pandas as pd
import os.path
from os import path as path_python

def get_longitud_latitud(departamento):
    coordenas = get_coordenadas(departamento);

    data = {
        'longitud': coordenas[0],
        'latitud': coordenas[1],
    }

    return data

def get_data(data):
    try:
        pattern = r"\s+"
        tweet_text_ = remove_emojis(data.replace('|', '')) # Remover emojis
        tweet_text_array = re.split(pattern, tweet_text_)
        tweet_text_array.pop(0) # Eliminar primer item que contiene AlertaAlbaKenneth
        dict_res = get_variables(tweet_text_array)
        return dict_res
    except Exception as e:
        dict_res = {
            "nombre": None,
            "edad": None,
            "fecha": None,
            "ubicacion": None,
            "departamento": None,
            "longitud": None,
            "latitud": None,
        }
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
    edad = 0
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
        edad = texto_sin_nombre[0].replace('de', '')
        edad = edad.replace('edad', '')
        if 'años' in edad:
            edad = edad.replace('años', '')
        elif 'meses' in edad:
            edad = edad.replace('meses', '')
            edad = int(edad)/12
        else:
            edad = 0
        texto_sin_nombre.pop(0)
        texto = " ".join(texto_sin_nombre)
    else:
        texto = texto_sin_nombre

    texto = texto.split(',')
    fecha = texto[0]
    fecha = fecha.replace('Desapareció el ', '')
    texto.pop(0)
    texto = " ".join(texto)
    texto = texto.split('Comparte')
    ubicacion = texto[0]
    ubicacion = ubicacion.replace('en', '')
    lugares = [item for item in ubicacion.split("  ") if item != '']
    if len(lugares) == 1:
        lugares = [item for item in ubicacion.split(" ") if item != '']
    departamento = lugares[-1]
    lugares.pop(-1)
    ubicacion = ", ".join(lugares)
    nombre = nombre.replace(",", "")

    geo_data = get_longitud_latitud(departamento.strip())

    dict_res = {
        "nombre": nombre.strip(),
        "edad": round(float(edad), 2),
        "fecha": fecha.strip(),
        "ubicacion": ubicacion.strip(),
        "departamento": departamento.strip(),
        "longitud": geo_data.get("longitud"),
        "latitud": geo_data.get("latitud"),
    }

    return dict_res