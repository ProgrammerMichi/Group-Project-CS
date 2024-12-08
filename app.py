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
st.set_page_config(page_title="Movie Recommender", page_icon="🎞️")

# Title & Intro
st.title("🎞️ Movie Recommender")
Instance = TMDbAPIClient("eb7ed2a4be7573ea9c99867e37d0a4ab")
st.write("hello!")
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    genre_check = st.checkbox("Genre")
    if genre_check:
        #This gives a list of movies according to which genre has been picked
        genrelist = Instance.get_genres(any)

        selgen = st.selectbox("Choose Genre", options = genrelist)
    else:
        st.write("nothing selected")


with col2:
    actor_check = st.checkbox("Actor")
    if actor_check:
        selactor = st.text_input("Write an actor whose movies you want to look for")
with col3:
    title_check = st.checkbox("Title")
with col4:
    keywords_check = st.checkbox("Keywords")
with col5:
    relate_check = st.checkbox("Based on other Movie")

left_column, right_column = st.columns([3,1])

if selgen:
        moviesbygenre = Instance.get_movie_by_genre_id(selgen,)
        
        for movie in moviesbygenre:
            st.write(f"{movie["title"]}")
else:
    continue

if selactor: 
        moviefound = Instance.search_movie_by_actors(selactor)
        if moviefound:
            for movie in moviefound:
                st.write(f"{movie["title"]}")
        else: 
            st.write("Couldn't find movies for this actor")
else: continue


selected = st.selectbox("Select Category", options= ["Genre", "Rating", "Actor","Length", "Keywords", "Recommendation", "Popular", "Title"])


if selected == "Genre":
   st.write("nüme")
        

if selected == "Rating":
    st.write(f"Rating")

if selected == "Actor":
    #This gives a list of Films according to the actor entered
    st.write("nah")
    
      

if selected == "Length":
    st.write(f"Length")

if selected == "Keywords":
    st.write(f"Keywords")

if selected == "Recommendation":
    st.write(f"Recommendation")

if selected == "Popular":
    st.write(f"Popular1")

if selected == "Title":
    user_input = st.text_input("With my Infinite knowledge I shall find a Movie that contains in its name the word you enter", value = None)
    if user_input:
        search_query = str(user_input)

        # Get the movies based on the search query
        movies = Instance.search_movie_title(search_query)
    
        # Display the movie titles
        for movie in movies:
            st.write(f"{movie['title']}")


