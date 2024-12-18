#This module is the connection point between code and the TMDB API
import streamlit as st
import requests
from tmdbv3api import TMDb, Movie, Genre, Discover, Person, Search
import sqlite3
import os
import json




#Instantiating the different APIs 
tmdb = TMDb()
tmdb.api_key = "eb7ed2a4be7573ea9c99867e37d0a4ab"
movie = Movie()
genre = Genre()
person = Person()
discover = Discover()
search = Search()


#List of all functions needed


def fetch_poster(movie_id):
    #Fetch the movie poster for the respective movie 
    movie_details = movie.details(movie_id)
    poster_path = movie_details.get('poster_path', None)
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


def fetch_movie_description(movie_id):
    #Fetch the movie description for the respective movie
    movie_details = movie.details(movie_id)
    overview = movie_details.get('overview', "No description available.")
    return overview


    
def get_genres():
    #Get a list of all available genres for the dropdown menu
    genres = genre.movie_list()
    genre_names = [i["name"] for i in genres]
    return genre_names


    
def get_genre_id(genre_name):
    #Get the id for a genre, later used to filter for a specific genre
    genres_response = genre.movie_list()
    for i in genres_response:
            if i["name"].lower() == genre_name.lower():
                return i["id"]


    
def search_actors(movie_id):
    #Get a list of first 7 actor of a movie

    movie_credits = movie.credits(movie_id)
    actors = movie_credits["cast"]
    bridge_actors = []
    return_actors = []
    for actor in actors:
        bridge_actors.append(actor["name"])
    return_actors = bridge_actors[:7]
    return return_actors
    

    
def get_movie_details(movie_id):
    #Get all movie details, so you can pick which information to use/present
    return movie.details(movie_id)


    
def get_keyword_id(term):
    #Get the id for a keyword, later used to filter for specific keyword
    keywords = search.keywords(term)
    if keywords:
        return keywords[0].id

# File path for ratings.json
RATINGS_FILE = os.path.join(os.path.dirname(__file__), "ratings.json")

# Load ratings from json file
def load_ratings():
    if not os.path.exists(RATINGS_FILE):
        return {}
    with open(RATINGS_FILE, "r") as file:
        return json.load(file)
    
    #Extract all unique movie titles from the ratings
    movies = set()
    for user_ratings in ratings.values():
        movies.update(user_ratings.keys())

    return list(movies), ratings  # Return movie titles and the ratings dictionary


#Gets current ratings of movies of users and lists them 
def get_user_movie_ratings():
    if "username" not in st.session_state:
        return []
    
    _, ratings = load_ratings()
    
    current_user = st.session_state["username"]
    user_ratings = ratings.get(current_user, {})
    
    movie_rating_list = [f"{movie}: {rating}" for movie, rating in user_ratings.items()]
    
    return movie_rating_list

#Save ratings to json file
def save_ratings(ratings):
    with open(RATINGS_FILE, "w") as file:
        json.dump(ratings, file, indent=4)


#update a user's rating for a movie
def add_rating(username, movie, rating):
    ratings = load_ratings()
    if username not in ratings:
        ratings[username] = {}
    ratings[username][movie] = rating
    save_ratings(ratings)


def findmovie(selgen, actor_check, selactor, keyword_check, selkeywords, excl_check, exclkeywords, selorder, rating_check, 
            selmin_rating, selmax_rating, selmin_votes, selmin_length, selmax_length, length_check, age_check, selage):
        #This function takes all input from the main page and, depending on whether they should be included, 
    #adds them to a dictionary, which is used by the tmdbv3api to get the wanted information
    #The dictionary is initally empty and depending on whether criteria has been selected (through checkmark or selection on dropdown menu)
    #or not. If criteria with textfield is included, try blocks first test if anything is found with entered words, return string
    #if it fails.
    #Returned data is stored in a variable, which will then be used to get the necessary information

    #ChatGPT gave the idea to use an empty dictionary

    search_parameters = {}

    if selgen != "None":
            search_parameters["with_genres"] = str(get_genre_id(selgen))
    

    if actor_check and selactor:
        try: 
            selactor_id = person.search(selactor + " ")
            search_parameters["with_cast"] = str(selactor_id[0].id)

        except: 
            st.write("**Actor not Included in Search**:")
            st.write("Actor not found, please adjust actor names")
        
        else:
            selactor_id = person.search(selactor + " ")
            search_parameters["with_cast"] = str(selactor_id[0].id)


    if keyword_check and selkeywords:
        try:
            search_parameters["with_keywords"] = str(get_keyword_id(selkeywords))

        except:
            st.write("**Keywords not implemented in search**:")
            st.write("Please only use one keyword. If you have already entered only one keyword, try changing it.")

        else:
            search_parameters["with_keywords"] = str(get_keyword_id(selkeywords))


    if excl_check and exclkeywords:
        try:
            search_parameters["without_keywords"] = str(get_keyword_id(exclkeywords))

        except:
            st.write("False Use of Keywords:")
            st.write("Please only use one Keyword, if you have already entered only one Keyword, try changing it.")

        else:
            search_parameters["without_keywords"] = str(get_keyword_id(exclkeywords))
    

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
        search_parameters["certification.lte"] = age
        search_parameters["certification_country"] = "DE"

    moviesfound = discover.discover_movies(search_parameters)
    return moviesfound



def search_movie(query):
    #Searches for movie titles fitting the input(query) and returns the movies with their data
    movieswtitle = search.movies(query)
    return movieswtitle

    

def movielist(returnmovies):
    #Checks whether list has been created, whether there is anything in it and then makes a list of the movies, if there are any

    #Test if variable returnmovies was created
    try:
        any(returnmovies)

    except:
        st.write("") 

    else:
        #Try block tests whether movies have been found
        try:
            for i in returnmovies:
                movie_id = str(i["id"])


        #Except block returns string in case the no movies are found
        except:
            st.write("No Movies Fitting the Criteria Found")


        #Else block creates for loop which creates a list of movies on the page,
        #including some information and option to rate the movie. 
        #Rating is stored on the site and fed into machine learning system to later be able to make a fitting recommendation
        else: 
            for i in returnmovies:
                
                #Design of each list entry, columns in order to have elements on the same line
                movielisting = st.container(border= True, height = 360)
                lc1, lc2, lc3, lc4, lc5 = movielisting.columns([0.5,1,1,1,1])

                #Storing movie id in variable for each loop, in order to use it as argument in later functions
                #Tried using movie["id"] directly instead of doing a detour with variable, gave an error in some places for some reason
                movie_id = str(i["id"])
                details = get_movie_details(movie_id)

                with lc1:
                    #Getting the poster and replacing it with text if not found
                    try:
                        poster_url = fetch_poster(movie_id)
                    except Exception: 
                        st.write(st.write("No Poster Available"))
                    else:
                        st.image(poster_url, caption=i["title"])

                        

                with lc2:
                    #Writes the movie title and offers option to read movie description with a button
                    st.write(f"**{details.title}**")
                    try:
                        description = fetch_movie_description(movie_id)
                        if not description: 
                            st.write("No Description Available")
                        else:
                            with st.popover("View Movie Description"):
                                st.write(description)
                    except Exception:
                        st.write("No Description Available")
                       


                with lc3:
                    #Lists first 7 listed actors, if available
                    st.write("**Lead Actors:**")
                    for i in search_actors(movie_id):
                        st.write(i)

                
                with lc4:
                    #Listing movie length in hours and minutes instead of only minutes
                    #Also lists release date

                    st.write("**Movie Length:**")
                    
                    length = details.runtime
                    st.write(str(length // 60),"hours", str(length % 60),"min")

                    st.text("")
                    st.text("")
                    st.text("")

                    st.write("**Release Date**")
                    st.write(str(details.release_date)) 

                with lc5:
                    #Lists rating of movie on TMDB, also offers the user to rate the movie
                    #Input of rating will then be used to recommend a movie for user
                    st.write("**TMDB Movie Rating**")
                    st.write(str(round(details.vote_average,1)))

                    st.text("")
                    st.text("")
                    st.text("")
                    
                    if st.session_state.get("logged_in", False):
                        movierating = st.slider("**Your Personal Rating**",min_value=0.5, max_value=5.0, key = movie_id, step= 0.1),
                        if st.button("Save Rating", key = "Rating for" + movie_id):
                            save_ratings(movierating[0])
                            if save_ratings:
                                st.write("Rating Saved!")
                    
                    else:
                        st.write("Log in to rate movies!")

                        
def store_rating(userId, movieId, rating):
    conn = sqlite3.connect("userratings.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS ratings (userId INTEGER, movieId INTEGER, rating REAL)")
    cursor.execute("INSERT INTO ratings (userId, movieId, rating) VALUES (?, ?, ?)", (userId, movieId, rating))
    conn.commit()
    conn.close()