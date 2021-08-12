#Python
import datetime
import re
import random

#3rd
import json
import tweepy
import pandas as pd
import os.path
from os import path as path_python

def get_longitud_latitud(departamento):
    deparamentos = {
        'Alta Verapaz': {
            'latitud': 15.47083,
            'longitud': -90.37083,
        },
        'Baja Verapaz': {
            'latitud': 15.10278,
            'longitud': -90.31806,
        },
        'Chimaltenango  ': {
            'latitud': 14.66111,
            'longitud': -90.81944,
        },
        'Chiquimula': {
            'latitud': 14.8,
            'longitud': -89.54583,
        },
        'Escuintla': {
            'latitud': 14.3009,
            'longitud': -90.78581,
        },
        'Guatemala': {
            'latitud': 15.783471,
            'longitud':  -90.230759,
        },
        'Huehuetenango': {
            'latitud': 15.31918,
            'longitud': -91.47241,
        },
        'Izabal': {
            'latitud': 15.5,
            'longitud': -89,
        },
        'Jalapa': {
            'latitud': 14.63472,
            'longitud': -89.98889,
        },
        'Jutiapa': {
            'latitud': 14.29167,
            'longitud': -89.89583,
        },
        'Petén': {
            'latitud': 16.7885,
            'longitud': -90.11698,
        },
        'El Progreso': {
            'latitud': 14.35,
            'longitud': -89.85,
        },
        'Quetzaltenango': {
            'latitud': 14.83472,
            'longitud': -91.51806,
        },
        'Quiché': {
            'latitud': 15.03085,
            'longitud': -91.14871,
        },
        'Retalhuleu': {
            'latitud': 14.533333,
            'longitud': -91.683333,
        },
        'Sacatepéquez': {
            'latitud': 14.718890,
            'longitud': -90.6441700,
        },
        'San Marcos': {
            'latitud': 14.96389,
            'longitud': -91.79444,
        },
        'Santa Rosa': {
            'latitud': 14.38806,
            'longitud': -90.29556,
        },
        'Sololá': {
            'latitud': 14.77222,
            'longitud': -91.18333,
        },
        'Suchitepéquez': {
            'latitud': 14.5333300,
            'longitud': -91.4166700,
        },
        'Totonicapán': {
            'latitud': 14.91167,
            'longitud': -91.36111,
        },
        'Zacapa': {
            'latitud': 14.97222,
            'longitud': -89.53056,
        },
    }

    actual = deparamentos.get('Guatemala')

    if departamento in deparamentos.keys():
        actual = deparamentos.get(departamento)

    number_latitud = random.uniform(-0.01, 0.24)
    number_longitud = random.uniform(-0.01, 0.24)

    latitud = actual.get('latitud') + number_latitud
    longitud = actual.get('longitud') + number_longitud

    data = {
        'latitud': latitud,
        'longitud': longitud
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
        edad = texto_sin_nombre[0].replace('de', '')
        edad = edad.replace('edad', '')
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
        "edad": edad.strip(),
        "fecha": fecha.strip(),
        "ubicacion": ubicacion.strip(),
        "departamento": departamento.strip(),
        "longitud": geo_data.get("longitud"),
        "latitud": geo_data.get("latitud"),
    }

    return dict_res