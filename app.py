import streamlit as st
from tmdbv3api import TMDb, Movie, Genre
import pandas
import numpy
import surprise
import os
from APIConnection import TMDBAPIClient

#This code will check whether code runs locally or on Streamlit, to decide whether .env file should be loaded, hopefully
# if os.getenv("STREAMLIT_SERVER") is None:
    # from dotenv import load_dotenv
    # load_dotenv()

user_input = st.text_input("With my Infinite knowledge I shall find a Movie that contains in its name the word you enter", value = None)
if user_input:
    testrun = TMDBAPIClient(eb7ed2a4be7573ea9c99867e37d0a4ab)
    search_query = str(user_input)
    movies = testrun.search_movie_title(search_query)
    return st.write(for movie in movies: print(f"Title: {movie["title"]}"))

st.write ("this updated")