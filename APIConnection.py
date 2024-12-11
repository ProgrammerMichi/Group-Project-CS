#This module is the connection point between code and the TMDB API
import streamlit as st
import requests
from tmdbv3api import TMDb, Movie, Genre, Discover, Person, Search



class TMDbAPIClient:
    def __init__(self, api_key="eb7ed2a4be7573ea9c99867e37d0a4ab"):
        self.tmdb = TMDb()
        self.tmdb.api_key = api_key
        self.movie = Movie()
        self.genre = Genre()
        self.person = Person()
        self.discover = Discover()
        self.search = Search()


    def fetch_poster(self, movie_id):
        url = "https://api.themoviedb.org/3/movie/" + movie_id + "?api_key=eb7ed2a4be7573ea9c99867e37d0a4ab&language=en-US"
        data = requests.get(url)
        data = data.json()
        poster_path = data['poster_path']
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        return full_path
    

    def fetch_movie_description(self, movie_id):
        url = f"https://api.themoviedb.org/3/movie/{str(movie_id)}?api_key=eb7ed2a4be7573ea9c99867e37d0a4ab&language=en-US"
        data = requests.get(url)
        data = data.json()
        overview = data.get('overview', "No description available.")
        return overview
    
    
    def get_genres(self, x = None):
        #Create a list with only genre names
        genres = self.genre.movie_list()
        genre_names = [genre["name"] for genre in genres]
        return genre_names
    
    
    def get_genre_id(self, genre_name):
        #Gets Genre id belonging to a certain genre
        genres = self.genre.movie_list()
        for genre in genres:
            if genre["name"].lower() == genre_name.lower():
                return genre["id"]
        return None
    
    
    def search_actors(self, movie_id):
        #Gets actors of a movie based on movie id
        movie_credits = self.movie.credits(movie_id)
        actors = movie_credits["cast"]
        bridge_actors = []
        return_actors = []
        for actor in actors:
            bridge_actors.append(actor["name"])
        return_actors = bridge_actors[:7]
        return return_actors
    

    def search_actor_id(self, actorname):
        #Gets Actor ID
        actor = self.person.search(actorname)
        if actor:
            actor_id = actor[0]["id"]
            return actor_id
        if not actor:
            return("no actors found")
        
    
    def get_movie_details(self, movie_id):
        #Gets information to a film
        return self.movie.details(movie_id)
    
    
    def get_keyword_id(self, search):
        keywords = self.search.keywords(search)
        if keywords:
            return keywords[0].id


Instance = TMDbAPIClient()

