#This module is the connection point between code and the TMDB API
import streamlit as st
import requests
from tmdbv3api import TMDb, Movie, Genre, Discover, Person, Search



class TMDbAPIClient:
    def __init__(self, api_key="eb7ed2a4be7573ea9c99867e37d0a4ab"):
        #Instantiating the different APIs 
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
    
    
        #Get a list of all available genres for the dropdown menu
    def get_genres(self, x = None):
        #Create a list with only genre names
        genres = self.genre.movie_list()
        genre_names = [genre["name"] for genre in genres]
        return genre_names
    
    
        #Get the id for a genre, later used to filter for a specific genre
    def get_genre_id(self, genre_name):
        #Gets Genre id belonging to a certain genre
        genres = self.genre.movie_list()
        for genre in genres:
            if genre["name"].lower() == genre_name.lower():
                return genre["id"]
        return None
    
    
        #Get a list of first 7 actor of a movie
    def search_actors(self, movie_id):
        movie_credits = self.movie.credits(movie_id)
        actors = movie_credits["cast"]
        bridge_actors = []
        return_actors = []
        for actor in actors:
            bridge_actors.append(actor["name"])
        return_actors = bridge_actors[:7]
        return return_actors
        
    
        #Get all movie details, so you can pick which information to use/present
    def get_movie_details(self, movie_id):
        #Gets information to a film
        return self.movie.details(movie_id)
    

        #Get the id for a keyword, later used to filter for specific keyword
    def get_keyword_id(self, search):
        keywords = self.search.keywords(search)
        if keywords:
            return keywords[0].id
        


    #This function takes all input from the main page and, depending on whether they should be included, 
    #adds them to a dictionary, which is used by the tmdbv3api to get the wanted information
    #The dictionary is initally empty and depending on whether criteria has been selected (through checkmark or selection on dropdown menu)
    #or not. If criteria with textfield is included, try blocks first test if anything is found with entered words, return string
    #if it fails.
    #Returned data is stored in a variable, which will then be used to get the necessary information

    #ChatGPT gave the idea to use an empty dictionary

    def findmovie(self, selgen, actor_check, selactor, keyword_check, selkeywords, excl_check, exclkeywords, selorder, rating_check, 
              selmin_rating, selmax_rating, selmin_votes, selmin_length, selmax_length, length_check, age_check, selage):
    
        search_parameters = {}

        if selgen != "None":
                search_parameters["with_genres"] = str(self.get_genre_id(selgen))
        

        if actor_check and selactor:
            try: 
                selactor_id = self.person.search(selactor + " ")
                search_parameters["with_cast"] = str(selactor_id[0].id)

            except: 
                st.write("**Actor not Included in Search**:")
                st.write("Actor not found, please adjust actor names")
            
            else:
                selactor_id = self.person.search(selactor + " ")
                search_parameters["with_cast"] = str(selactor_id[0].id)


        if keyword_check and selkeywords:
            try:
                search_parameters["with_keywords"] = str(self.get_keyword_id(selkeywords))

            except:
                st.write("**Keywords not implemented in search**:")
                st.write("Please only use one keyword. If you have already entered only one keyword, try changing it.")

            else:
                search_parameters["with_keywords"] = str(self.get_keyword_id(selkeywords))


        if excl_check and exclkeywords:
            try:
                search_parameters["without_keywords"] = str(self.get_keyword_id(exclkeywords))

            except:
                st.write("False Use of Keywords:")
                st.write("Please only use one Keyword, if you have already entered only one Keyword, try changing it.")

            else:
                search_parameters["without_keywords"] = str(self.get_keyword_id(exclkeywords))
        

        if selorder == "Descending":
            search_parameters["sort_by"] = "vote_average.desc"

        else:
            search_parameters["sort_by"] = "vote_average.asc"
        

        if rating_check:
            search_parameters["vote_average.gte"] = str(selmin_rating)
            search_parameters["vote_average.lte"] = str(selmax_rating)
            search_parameters["vote_count.gte"] = str(selmin_votes)


        if length_check:
            search_parameters["with_runtime.gte"] = str(selmin_length)
            search_parameters["with_runtime.lte"] = str(selmax_length)

        if age_check and selage:
            age = selage.strip("FSK ")
            
            search_parameters["certification"] = age
            search_parameters["certification_country"] = "DE"

        moviesfound = self.discover.discover_movies(search_parameters)
        return moviesfound
    
        

Instance = TMDbAPIClient()

