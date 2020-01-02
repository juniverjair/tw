from django.shortcuts import render
import tweepy
from tweepy.auth import OAuthHandler
from .models import Sorteo, Tweet

import random
from django.http import JsonResponse

from django.core import serializers
from django.http import HttpResponse

# Create your views here.

def home_timeline(request):
    consumer_key = 'kYSaJgciJufyHGTHfOqeowUIp'
    consumer_secret = 'YMeCmVmqae9PlkagOCz9FcxQf38sjrG6zi3QmNWZar6V9LPNhh'
    access_token = '179317665-cdjLp9p2wW3sWCfkwzg0eMtfRJsFDItbhbYibWzE'
    access_token_secret = 'bE1XP5Nf5RCqBVNgYW6KI61qlW4BUcudbMKR8RqPPxSA0'
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)

    seleccionados = []

    #for tweet in tweepy.Cursor(api.search, q="#ESPOL", count=5, result_type = 'recent').items():
    for tweet in api.search(q = "#ESPOL -filter:retweets", count = 5, result_type = 'recent', tweet_mode="extended"):

        seleccionados.append({"usuario": tweet.user.screen_name, "fecha":tweet.created_at, "texto": tweet.full_text})

    return render(request, 'public_tweets.html', {"public_tweets": seleccionados})


def tweetsCargar(request):

    id = request.POST["sorteo"]

    tweets = Tweet.objects.filter(sorteo=id)
    sorteo = Sorteo.objects.filter(id=id)

    ganador_tweet_id = ""
    ganador = ""

    for d in sorteo:
        ganador_tweet_id = d.ganador
    
    if ganador_tweet_id != "":
         tweet_ganador = Tweet.objects.filter(id=ganador_tweet_id)
         for k in tweet_ganador:
             ganador = k.fecha + " " + k.usuario + " " + k.texto

    lista_sorteos = []


    for s in tweets:
        
        lista_sorteos.append({
            "id" : s.id,
            "usuario" : s.usuario,
            "fecha" : s.fecha,
            "texto" : s.texto,
        })

    

    return render(request, 'public_tweets.html', {"public_tweets": lista_sorteos, "sorteo": id,  "ganador": ganador})

def encontrarGanador(request):

    id = request.POST["sorteo"]

    sorteo = Sorteo.objects.filter(id=id)
    sh = Sorteo.objects.get(id=id)

    lista_sorteos = []

    existe_ganador = False

    for i in sorteo:
        if i.ganador != "":
            existe_ganador = True
            ganador = "Ya existe un ganador!"
    
    if existe_ganador == False:

        tweets = Tweet.objects.filter(sorteo=id)

        

        for s in tweets:
            
            lista_sorteos.append({
                "id" : s.id,
                "usuario" : s.usuario,
                "fecha" : s.fecha,
                "texto" : s.texto,
            })

        aleatorio = random.choice(lista_sorteos)

        sh.ganador = aleatorio["id"]
        sh.save()

        ganador = aleatorio["fecha"] + " " + aleatorio["usuario"] + " " + aleatorio["texto"]

    return render(request, 'public_tweets.html', {"public_tweets": lista_sorteos, "sorteo": id, "ganador": ganador})




def sorteosCargar(request):
    sorteos = Sorteo.objects.all()
    lista_sorteos = []

    for s in sorteos:
        lista_sorteos.append({
            "id" : s.id,
            "nombre" : s.nombre,
            "fecha" : s.fecha,
            "ganador" : s.ganador,
            "hashtag" : s.hashtag,
        })
    lista_sorteos.reverse()

    return render(request, 'sorteos.html', {"sorteos": lista_sorteos})

def sorteosCrear(request):

    nombre = request.POST["nombre"]
    hashtag = request.POST["hashtag"]

    u = Sorteo(nombre=nombre, hashtag=hashtag)
    u.save()


    consumer_key = 'kYSaJgciJufyHGTHfOqeowUIp'
    consumer_secret = 'YMeCmVmqae9PlkagOCz9FcxQf38sjrG6zi3QmNWZar6V9LPNhh'
    access_token = '179317665-cdjLp9p2wW3sWCfkwzg0eMtfRJsFDItbhbYibWzE'
    access_token_secret = 'bE1XP5Nf5RCqBVNgYW6KI61qlW4BUcudbMKR8RqPPxSA0'
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)

    #seleccionados = []

    #for tweet in tweepy.Cursor(api.search, q="#ESPOL", count=5, result_type = 'recent').items():
    for tweet in api.search(q = hashtag + " -filter:retweets", count = 20, result_type = 'recent', tweet_mode="extended"):

        #seleccionados.append({"usuario": tweet.user.screen_name, "fecha":tweet.created_at, "texto": tweet.full_text})

        k = Tweet(usuario=tweet.user.screen_name, fecha=tweet.created_at, texto=tweet.full_text, sorteo=u)
        k.save()


    sorteos = Sorteo.objects.all()

    lista_sorteos = []

    for s in sorteos:
        lista_sorteos.append({
            "id" : s.id,
            "nombre" : s.nombre,
            "fecha" : s.fecha,
            "ganador" : s.ganador,
            "hashtag" : s.hashtag,
        })

    lista_sorteos.reverse()

    return render(request, 'sorteos.html', {"sorteos": lista_sorteos})