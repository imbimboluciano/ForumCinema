from forum.models import *
from PyMovieDb import IMDB
import json
import requests



def citazione_table():

    citazioni_list = ["You talking to me?", "May the Force be with you.", "Life was like a box of chocolates. You never know what you’re gonna get.", 
                      "After all, tomorrow is another day.", "I’m going to make him an offer he can’t refuse.", "E.T. phone home.", "My name is Bond, James Bond.", 
                      "The first rule of Fight Club is: You do not talk about Fight Club."]
    for i in range(len(citazioni_list)):
        citazione = Citazione()
        citazione.descrizione = citazioni_list[i]
        citazione.save()

def erase_movie_table():
    CinemaClub.objects.all().delete()
   



def init_movie_table():
    url_image = "https://image.tmdb.org/t/p/original"
    url = 'https://api.themoviedb.org/3/discover/movie?api_key=7ca868b93903d6d7ee6c0e9f5428ba7c&primary_release_year=2023&sort_by=revenue.desc&include_all_movies=true'
    response = requests.get(url)
    response_json = response.json()
    response_str = json.dumps(response_json)
    movies = json.loads(response_str)
    for movie in movies["results"]:
        m = Movie()
        m.titolo = movie["title"]
        m.anno = movie["release_date"]
        m.poster = url_image + movie["poster_path"]
        m.save()


def init_avatar_table():
    url_image = "https://image.tmdb.org/t/p/original"
    url = 'https://api.themoviedb.org/3/discover/movie?api_key=7ca868b93903d6d7ee6c0e9f5428ba7c&primary_release_year=2023&sort_by=revenue.desc&include_all_movies=true'
    response = requests.get(url)
    response_json = response.json()
    response_str = json.dumps(response_json)
    movies = json.loads(response_str)
    for movie in movies["results"]:
        avatar = Avatar()
        avatar.image = url_image + movie["backdrop_path"]
        avatar.save()

    
