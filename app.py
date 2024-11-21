import streamlit as st
from streamlit_option_menu import option_menu
from tmdbv3api import TMDb, Movie, Genre
#import pandas
#import numpy
#import surprise
#import os
from APIConnection import TMDbAPIClient

with st.sidebar:
    selected = option_menu(
        menu_title = "Select Category"
        options = ["Genre", "Rating", "Actors","Length", "Keywords", "Recommendation", "Popular", "Title"]
    )

if selected == "Genre":
    st.write(f"Genre")

if selected == "Rating":
    st.write(f"Rating")

if selected == "Actors":
    st.write(f"Actors")

if selected == "Length":
    st.write(f"Length")

if selected == "Keywords":
    st.write(f"Keywords")

if selected == "Recommendation"
    st.write(f"Recommendation")

if selected == "Popular"
    st.write(f"Popular")

if selected == "Title"
user_input = st.text_input(value = None)
if user_input:
    # Initialize the TMDB API client with the API key
    testrun = TMDbAPIClient("eb7ed2a4be7573ea9c99867e37d0a4ab")
    search_query = str(user_input)
    
    # Get the movies based on the search query
    movies = testrun.search_movie_title(search_query)
    
    # Display the movie titles
    for movie in movies:
        st.write(f"{movie['title']}")


