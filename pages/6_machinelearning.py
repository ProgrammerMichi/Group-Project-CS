import streamlit as st
from tmdbv3api import TMDb, Movie, Genre, Discover, Person
from APIConnection import TMDbAPIClient
import pandas as pd
import numpy as np
import os

# Tab Title
st.set_page_config(page_title="Movie Recommender", page_icon="🎥", layout="wide")

# Title & Intro
st.markdown(
    """
    <style>
        .main-title {
            font-size: 50px;
            font-weight: bold;
            color: #FF5733;
            text-align: center;
        }
        .sub-title {
            font-size: 18px;
            color: #555;
            text-align: center;
        }
        .movie-poster {
            border-radius: 10px;
        }
        .top-rec-container {
            border-radius: 15px;
            padding: 20px;
            color: white;
            background-size: cover;
            text-shadow: 2px 2px 5px black;
        }
    </style>
    <h1 class="main-title">Movie Recommender 🎥</h1>
    <p class="sub-title">Your personalized guide to the best movies!</p>
    """,
    unsafe_allow_html=True,
)

Instance = TMDbAPIClient("eb7ed2a4be7573ea9c99867e37d0a4ab")

# File path to save ratings
RATINGS_FILE = "user_ratings.csv"

# Load existing ratings or initialize empty DataFrame
if os.path.exists(RATINGS_FILE):
    user_ratings = pd.read_csv(RATINGS_FILE)
else:
    user_ratings = pd.DataFrame(columns=["userId", "movieId", "rating"])

# Sidebar for filters
with st.sidebar:
    st.markdown("### 🎬 Filters")
    genre_check = st.checkbox("Filter by Genre")
    if genre_check:
        genrelist = ["Select"]
        gl = list(Instance.get_genres(any))
        for i in gl:
            genrelist.append(i)
        selgen = st.selectbox("Choose Genre", options=genrelist)

    actor_check = st.checkbox("Filter by Actor")
    if actor_check:
        selactor = st.text_input("Enter Actor's Name")

    keyword_check = st.checkbox("Include Keywords")
    if keyword_check:
        selkeywords = st.text_input("Enter Keywords")

    excl_check = st.checkbox("Exclude Keywords")
    if excl_check:
        exclkeywords = st.text_input("Enter Excluded Keywords")

    rating_check = st.checkbox("Filter by Ratings")
    if rating_check:
        selmin_rating = st.slider("Minimum Rating", 0.0, 10.0, 5.0, 0.1)
        selmax_rating = st.slider("Maximum Rating", 0.0, 10.0, 10.0, 0.1)

    st.markdown("---")
    selorder = st.selectbox("Sort By", ["Descending", "Ascending"])

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
    if rating_check:
        search_parameters["vote_average.gte"] = str(selmin_rating)
        search_parameters["vote_average.lte"] = str(selmax_rating)
    if selorder == "Descending":
        search_parameters["sort_by"] = "vote_average.desc"
    else:
        search_parameters["sort_by"] = "vote_average.asc"

    moviesfound = Instance.discover.discover_movies(search_parameters)
    return moviesfound

# Function to calculate recommendation scores
def calculate_score(movie, user_id, user_ratings, tmdb_rating_weight=0.4, personal_rating_weight=0.3, similar_rating_weight=0.3):
    movie_id = movie["id"]
    tmdb_rating = movie.get("vote_average", 0)
    
    # User's personal rating for this movie
    personal_rating = user_ratings[(user_ratings["userId"] == user_id) & (user_ratings["movieId"] == movie_id)]["rating"].mean()
    personal_rating = personal_rating if not np.isnan(personal_rating) else 0

    # Final weighted score
    score = (
        tmdb_rating_weight * tmdb_rating +
        personal_rating_weight * personal_rating
    )
    return score

# Top Recommendation Section
def display_top_recommendation(movie):
    poster_url = Instance.fetch_poster(movie["id"])
    st.markdown(
        f"""
        <div class="top-rec-container" style="background-image: url('{poster_url}')">
            <h1>{movie['title']}</h1>
            <p>TMDB Rating: {movie.get('vote_average', 'N/A')}</p>
            <p>{movie.get('overview', 'No overview available.')}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Display Movies in a Grid
def display_movie_grid(movies):
    cols = st.columns(5)
    for i, movie in enumerate(movies):
        with cols[i % 5]:
            try:
                poster_url = Instance.fetch_poster(movie["id"])
                st.image(poster_url, use_column_width=True, caption=movie["title"])
            except:
                st.write(movie["title"])

# Main Section
returnmovies = findmovie()
if returnmovies:
    st.markdown("### 🎥 Top Recommendation 🎥")
    display_top_recommendation(returnmovies[0])

    st.markdown("### 🎬 More Recommendations 🎬")
    display_movie_grid(returnmovies[1:])

    # Rating Section
    st.markdown("### ⭐ Rate Movies")
    for movie in returnmovies:
        movie_id = movie["id"]
        rating = st.slider(f"Rate {movie['title']}", 1, 10, key=f"slider_{movie_id}")
        if st.button(f"Save Rating for {movie['title']}", key=f"button_{movie_id}"):
            new_rating = pd.DataFrame({"userId": [1], "movieId": [movie_id], "rating": [rating]})
            user_ratings = pd.concat([user_ratings, new_rating], ignore_index=True)
            user_ratings.to_csv(RATINGS_FILE, index=False)
            st.success(f"Rating saved for {movie['title']}")