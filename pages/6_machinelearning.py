import streamlit as st
from tmdbv3api import TMDb, Movie, Genre, Discover, Person
from APIConnection import TMDbAPIClient
import pandas as pd
import numpy as np
import os

# TMDb Base URL for Images
IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"

# Tab Title
st.set_page_config(page_title="Movie Recommender", page_icon="🎞️", layout="wide")

# Title & Intro
st.title("🎞️ Movie Recommender")

Instance = TMDbAPIClient("eb7ed2a4be7573ea9c99867e37d0a4ab")

st.markdown("**Welcome to your personalized movie recommender!**")

# File path to save ratings
RATINGS_FILE = "user_ratings.csv"

# Load existing ratings or initialize empty DataFrame
if os.path.exists(RATINGS_FILE):
    user_ratings = pd.read_csv(RATINGS_FILE)
else:
    user_ratings = pd.DataFrame(columns=["userId", "movieId", "rating"])

# Helper function to get the full poster URL
def get_poster_url(poster_path):
    if poster_path:
        return f"{IMAGE_BASE_URL}{poster_path}"
    return None

# Helper function to create bordered content
def bordered_container(content_html):
    return f"""
    <div style="
        border: 1px solid #ddd;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 15px;
    ">
        {content_html}
    </div>
    """

# Columns for filter options
col1, col2, col3, col4, col5, col6, col7 = st.columns([2, 2, 2, 2, 2, 3, 3])

with col1:
    genre_check = st.checkbox("Genre")
    if genre_check:
        genrelist = ["Select"]
        gl = list(Instance.get_genres(any))
        for i in gl:
            genrelist.append(i)
        selgen = st.selectbox("Choose Genre", options=genrelist)

with col2:
    actor_check = st.checkbox("Actor")
    if actor_check:
        selactor = st.text_input("Choose Actor")

with col3:
    keyword_check = st.checkbox("Include Keywords")
    if keyword_check:
        selkeywords = st.text_input("Enter Keywords", key=1)

with col4:
    excl_check = st.checkbox("Exclude Keywords")
    if excl_check:
        exclkeywords = st.text_input("Enter Keywords", key=2)

with col5:
    selorder = st.selectbox("Order of Movies by Ratings", ["Descending", "Ascending"])

with col6:
    leftbox = col6.container()
    l1, l2 = leftbox.columns(2)
    with l1:
        st.write("Ratings")
    with l2:
        rating_check = st.checkbox("Apply Ratings")

    col6_1, col6_2 = leftbox.columns(2)
    with col6_1:
        selmin_rating = st.number_input("Minimum Rating", min_value=0.0, max_value=10.0, step=0.1, format="%0.1f")
    with col6_2:
        selmax_rating = st.number_input("Maximum Rating", min_value=0.0, max_value=10.0, value=10.0, step=0.1, format="%0.1f")

    selmin_votes = leftbox.number_input("Minimum Amount of Ratings", min_value=0, value=1000)

with col7:
    midbox = col7.container()
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

    underbox = col7.container()
    m3, m4 = underbox.columns(2)
    with m3:
        st.write("Movie Restrictions")
    with m4:
        st.checkbox("Apply Restriction:")
    col7_3 = underbox.columns(1)
    with col7_3[0]:
        st.checkbox("Exclude 18+ Movies")

# Function to fetch movies based on filters
def findmovie():
    search_parameters = {}
    if genre_check and selgen != "Select":
        search_parameters["with_genres"] = str(Instance.get_genre_id(selgen))
    if actor_check and selactor:
        selactor_id = Instance.person.search(selactor)
        search_parameters["with_cast"] = str(selactor_id[0].id)
    if keyword_check and selkeywords:
        search_parameters["with_keywords"] = str(Instance.get_keyword_id(selkeywords))
    if excl_check and exclkeywords:
        search_parameters["without_keywords"] = str(Instance.get_keyword_id(exclkeywords))
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

    moviesfound = Instance.discover.discover_movies(search_parameters)
    return moviesfound

# Get movies based on filters
returnmovies = findmovie()

# Display movies with borders
if returnmovies:
    for movie in returnmovies:
        poster_url = get_poster_url(movie.get("poster_path"))
        content = f"""
        <h4>{movie['title']}</h4>
        <img src="{poster_url}" alt="Poster" style="width: 100%; border-radius: 5px; margin-bottom: 10px;">
        <p>TMDB Rating: {movie.get('vote_average', 'N/A')}</p>
        """
        st.markdown(bordered_container(content), unsafe_allow_html=True)