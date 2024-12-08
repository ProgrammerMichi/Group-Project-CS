#This module is the connection point between code and the TMDB API
import streamlit as st
from tmdbv3api import TMDb, Movie, Genre, Discover, Person

tmdb = TMDb()
tmdb.api_key = "eb7ed2a4be7573ea9c99867e37d0a4ab"


#This code, in the future, should check whether code runs locally or on Streamlit, to decide whether .env file should be loaded, hopefully
# if os.getenv("STREAMLIT_SERVER") is None:
    # from dotenv import load_dotenv
    # load_dotenv()

class TMDbAPIClient:
    def __init__(self, api_key=None):
        self.tmdb = TMDb()

        #The API_Key should be either implemented through an environment variable or streamlit/github secrets
        self.tmdb.api_key = api_key
        self.movie = Movie()
        self.genre = Genre()
        self.person = Person()
        self.discover = Discover()


    def search_movie_title(self, query):
        #Looks for a movie title based on query
        return self.movie.search(query)
    
    
    def get_genres(self, movie_genre):
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
    
    
    def get_movie_by_genre_id(self, genre_name, page=1,):
        #Looks for movies according to genre id
        genre_id = self.get_genre_id(genre_name)
        

        movies = self.discover.discover_movies({
            "with_genres": genre_id,
            "page": page,
            "with_original_language": "en",
            "sort_by": "vote_average.desc",
            "vote_count.gte" : 1000
    
        })
        return movies
        
    
    
    def search_actors(self, movie_id):
        #Gets actors of a movie based on movie id
        movie_details = self.movie.details(movie_id)
        return movie_details.get("cast",[])
    
    def search_movie_by_actors(self, actorname, page = 1):
        #Gets Actor ID
        actor = self.person.search(actorname)
        if actor:
            actor_id = actor[0]["id"]
        if not actor:
            return []

        #Gets movie based on Actor ID
        actormovies = self.discover.discover_movies({
            "with_cast": actor_id,
            "sort_by": "vote_average_desc.",
            "page": page,
            "with_original_language": "en"
        })
        return actormovies

    def search_movie_length(self, min_length, max_length):
        #Looks for a movie depending on length
        moviesbeforefilter = self.movie.popular()
        filtered_movies = [movie for movie in moviesbeforefilter
                           if min_length <= movie["runtime"] <= max_length]
        return filtered_movies
    
        
    def search_movie_by_keywords(self, keyword):
        #Looks for a movie depending on keywords
        return self.movie.keywords(keyword)
    
    
    def get_movie_details(self, movie_id):
        #Gets information to a film
        return self.movie.details(movie_id)
    
    
    def get_recommendations(self, movie_id):
        #Generates a recommendation based on a movie
        return self.movie.recommendations(movie_id)
    
    
    def get_popular_movie(self):
        #List of most popular films
        return self.movie.popular()



