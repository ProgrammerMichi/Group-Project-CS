import streamlit as st
from streamlit_option_menu import option_menu
from tmdbv3api import TMDb, Movie, Genre, Discover, Person
#import pandas
#import numpy
#import surprise
#import os
from APIConnection import TMDbAPIClient
import pandas as pd
import numpy as np

# Tab Title
st.set_page_config(page_title="Movie Recommender", page_icon="🎞️", layout="wide")

# Title & Intro
st.title("🎞️ Movie Recommender")

Instance = TMDbAPIClient("eb7ed2a4be7573ea9c99867e37d0a4ab")

st.markdown("**hello!**")

col1, col2, col3, col4, col5, col6, col7, col8 = st.columns([2,2,2,2,2,3,3,3])

with col1:
    genre_check = st.checkbox("Genre")
    if genre_check:
        #This gives a list of movies according to which genre has been picked
        genrelist = ["Select"]
        gl = list(Instance.get_genres(any))
        for i in gl:
            genrelist.append(i)
        selgen = st.selectbox("Choose Genre", options = genrelist)
    

with col2:
    actor_check = st.checkbox("Actor")
    if actor_check:
        selactor = st.text_input("Choose Actor")

with col3:
    keyword_check = st.checkbox("Keywords")
    if keyword_check:
        selkeywords = st.text_input("Enter Keywords")
    

with col4:
    relate_check = st.checkbox("Similar")

with col5:
    selorder = st.selectbox("Order of Movies by Ratings", ["Descending", "Ascending"])

with col6:
    leftbox = col6.container(border=True, height=275)

    l1, l2 = leftbox.columns(2)
    with l1:
        st.write ("Ratings")
    with l2:
        rating_check = st.checkbox("Apply Ratings")

    col6_1, col6_2 = leftbox.columns(2)

    with col6_1:
        selmin_rating = st.number_input("Minimum Rating", min_value=0.0, max_value=10.0, step = 0.1, format = "%0.1f")

    with col6_2:
        selmax_rating = st.number_input("Maximum Rating", min_value=0.0, max_value=10.0, value = 10.0, step = 0.1, format = "%0.1f" )

selmin_votes = leftbox.number_input("Minimum Amount of Ratings", min_value=0, value= 1000)
    
    
with col7:
    midbox = col7.container(border=True, height=200)

    m1, m2 = midbox.columns(2)
    with m1:
        st.write("Length")
    with m2:
        length_check = st.checkbox("Apply Length")

    col7_1, col7_2 = midbox.columns(2)

    with col7_1:
        selmin_length = st.number_input("Minimum Length (in min)", min_value=0)

    with col7_2:
        selmax_length = st.number_input("Maximum Length (in min)", min_value=0)


with col8:
    rightbox = col8.container(border=True, height= 200)
    r1, r2 = rightbox.columns(2)
    with r1:
        st.write("Release Date")
    with r2:
        date_check = st.checkbox("Apply Date")

    col8_1, col8_2 = rightbox.columns(2)
    with col8_1:
        selrel_after = st.date_input("Released After:")
    with col8_2:
        selrel_before = st.date_input("Released Before:")

 #ChatGPT helped with basic idea of this function(how to manage input that can be turned on/off)   
def findmovie():
    search_parameters = {}
    if genre_check and selgen != "Select":
            search_parameters["with_genres"] = str(Instance.get_genre_id(selgen))
    
    if actor_check and selactor: 
        selactor_id = Instance.person.search(selactor)
        search_parameters["with_cast"] = str(selactor_id[0].id)

    if keyword_check and selkeywords:
        keyword_ids = selkeywords
        search_parameters["with_keywords"] = str(keyword_ids.lower)
    
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
        search_parameters["with_runtime.lte"] = str(selmin_length)

    if date_check:
        search_parameters["primary_release_date.gte"] = str(selrel_after)
        search_parameters["primary_release_date.lte"] = str(selrel_before) 

    moviesfound = Instance.discover.discover_movies(search_parameters)

    return moviesfound

returnmovies = findmovie()
if returnmovies:
    cols = st.columns(5)
    for movie in returnmovies:
        movie_id = int(movie["id"])
        st.write(movie_id)
        st.write(f"{movie["title"]}, {movie["id"]}")
        poster_url = Instance.fetch_poster(movie_id)
        st.image(poster_url, caption=movie["title"], use_column_width=True)
        
       



        
