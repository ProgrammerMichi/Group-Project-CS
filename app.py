import streamlit as st
from streamlit_option_menu import option_menu
from tmdbv3api import TMDb, Movie, Genre
#import pandas
#import numpy
#import surprise
#import os
from APIConnection import TMDbAPIClient

selected = st.selectbox("Select Category", options= ["Genre", "Rating", "Actor","Length", "Keywords", "Recommendation", "Popular", "Title"])
if selected:
    st.write(selected)
    # Initialize the TMDB API client with the API key
    Instance = TMDbAPIClient("eb7ed2a4be7573ea9c99867e37d0a4ab")


if selected == "Genre":
    st.write(f"wos")
    selgen = st.selectbox("Choose Genre", options= [Instance.movie_list()])        
    ])


if selected == "Rating":
    st.write(f"Rating")

if selected == "Actors":
    st.write(f"Actors")

if selected == "Length":
    st.write(f"Length")

if selected == "Keywords":
    st.write(f"Keywords")

if selected == "Recommendation":
    st.write(f"Recommendation")

if selected == "Popular":
    st.write(f"Popular")

if selected == "Title":
    user_input = st.text_input("With my Infinite knowledge I shall find a Movie that contains in its name the word you enter", value = None)
    if user_input:
        search_query = str(user_input)

        # Get the movies based on the search query
        movies = Instance.search_movie_title(search_query)
    
        # Display the movie titles
        for movie in movies:
            st.write(f"{movie['title']}")


