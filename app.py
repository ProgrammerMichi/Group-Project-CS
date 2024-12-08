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

col0, col1, col2, col3, col4, col5, col6, col7, col8 = st.columns([2,2,2,2,2,2,1,3,3])

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

with col7:
    leftbox = col7.container(border=True, height=150)

    l1, l2 = leftbox.columns(2)
    with l1:
        st.write ("Ratings")
    with l2:
        st.checkbox("Apply")

    col7_1, col7_2 = leftbox.columns(2)

    with col7_1:
        minrating = st.number_input("Minimum Rating", min_value=0, max_value=100)

    with col7_2:
        st.number_input("Maximum Rating", min_value=minrating, max_value=100)
    
with col8:
    rightbox = col8.container(border=True, height=150)
    rightbox.write("Length")

    col8_1, col8_2 = rightbox.columns(2)

    with col8_1:
        minlength = st.number_input("Minimum Length (in min)", min_value=0)

    with col8_2:
        st.number_input("Maximum Length (in min)", min_value=minlength)
    
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
    st.write("moin")


