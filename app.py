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

col0, col1, col2, col3, col4, col5, col6, col7 = st.columns([2,2,2,2,2,2,3,3])

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
    keywords_check = st.checkbox("Keywords")
    

with col4:
    relate_check = st.checkbox("Similar")

with col5:
    title_check = st.checkbox("Title")
    if title_check:
        title_input = st.text_input("Write the Title", value = None)
        if title_input:
            global search_query
            search_query = str(title_input)

with col6:
    leftbox = col6.container(border=True, height=260)

    l1, l2 = leftbox.columns(2)
    with l1:
        st.write ("Ratings")
    with l2:
        rat_ch = st.checkbox("Apply Ratings")

    col6_1, col6_2 = leftbox.columns(2)

    with col6_1:
        minrating = st.number_input("Minimum Rating", min_value=0, max_value=100)

    with col6_2:
        maxrating = st.number_input("Maximum Rating", min_value=minrating, max_value=100)

minvotes = leftbox.number_input("Minimum Amount of Ratings", min_value=0, value= 1000)
    
    
with col7:
    rightbox = col7.container(border=True, height=200)

    r1, r2 = rightbox.columns(2)
    with r1:
        st.write("Length")
    with r2:
        len_ch = st.checkbox("Apply Length")

    col7_1, col7_2 = rightbox.columns(2)

    with col7_1:
        minlength = st.number_input("Minimum Length (in min)", min_value=0)

    with col7_2:
        maxlength = st.number_input("Maximum Length (in min)", min_value=minlength)
    
alt1, alt2 = st.columns([2,17])
with alt2:
    if genre_check:
        if selgen != "Select":
            moviesbygenre = Instance.get_movie_by_genre_id(selgen)
        
            for movie in moviesbygenre:
                st.write(f"{movie["title"]}")
                


    if actor_check:
        if selactor: 
            moviefound = Instance.search_movie_by_actors(selactor)
            if moviefound:
                for movie in moviefound:
                    st.write(f"{movie["title"]}")
            else: 
                st.write("Couldn't find movies for this actor")

    if title_check:
        if title_input:
            movies = Instance.search_movie_title(search_query)
            for movie in movies:
                st.write(f"{movie['title']}")
