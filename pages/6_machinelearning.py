import streamlit as st
from tmdbv3api import TMDb, Movie, Genre, Discover, Person
from APIConnection import TMDbAPIClient
import pandas as pd
import numpy as np
import os

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

    moviesfound = Instance.discover.discover_movies(search_parameters)
    return moviesfound

# Function to calculate weighted recommendation scores
def calculate_score(movie, user_id, user_ratings, tmdb_rating_weight=0.4, personal_rating_weight=0.3, similar_rating_weight=0.3):
    movie_id = movie["id"]
    tmdb_rating = movie.get("vote_average", 0)
    
    # User's personal rating for this movie
    personal_rating = user_ratings[(user_ratings["userId"] == user_id) & (user_ratings["movieId"] == movie_id)]["rating"].mean()
    personal_rating = personal_rating if not np.isnan(personal_rating) else 0

    # Average rating of similar movies
    similar_movies = user_ratings[user_ratings["movieId"].isin(get_similar_movies(movie))]
    similar_rating = similar_movies["rating"].mean()
    similar_rating = similar_rating if not np.isnan(similar_rating) else 0

    # Final weighted score
    score = (
        tmdb_rating_weight * tmdb_rating +
        personal_rating_weight * personal_rating +
        similar_rating_weight * similar_rating
    )
    return score

# Function to get similar movies (based on genre, actor, etc.)
def get_similar_movies(movie):
    # For simplicity, let's match movies by genre
    genre_ids = movie.get("genre_ids", [])
    similar_movies = user_ratings[user_ratings["movieId"].isin(
        [m["id"] for m in returnmovies if set(genre_ids).intersection(m.get("genre_ids", []))]
    )]
    return similar_movies["movieId"].tolist()

returnmovies = findmovie()

# Allow users to rate movies
if returnmovies:
    for movie in returnmovies:
        movielisting = st.container()
        lc1, lc2, lc3 = movielisting.columns([1.3, 3, 2])
        movie_id = movie["id"]

        with lc1:
            try:
                poster_url = Instance.fetch_poster(movie_id)
                st.image(poster_url, caption=movie["title"], use_column_width=True)
            except:
                st.write("No Poster Available")

        with lc2:
            st.write(f"**{movie['title']}**")
            st.write(f"TMDB Rating: {movie.get('vote_average', 'N/A')}")

        with lc3:
            rating = st.slider(f"Rate {movie['title']}", 1, 10, key=f"slider_{movie_id}")
            if st.button(f"Save Rating for {movie['title']}", key=f"button_{movie_id}"):
                new_rating = pd.DataFrame({"userId": [1], "movieId": [movie_id], "rating": [rating]})
                user_ratings = pd.concat([user_ratings, new_rating], ignore_index=True)
                user_ratings.to_csv(RATINGS_FILE, index=False)  # Save ratings to CSV
                st.success(f"Rating saved for {movie['title']}")

# Display recommendations
if st.sidebar.button("Get Recommendations"):
    user_id = 1
    recommendations = []
    for movie in returnmovies:
        score = calculate_score(movie, user_id, user_ratings)
        recommendations.append((movie, score))

    # Sort recommendations by score
    recommendations = sorted(recommendations, key=lambda x: x[1], reverse=True)[:5]

    st.sidebar.markdown("### Recommended Movies:")
    for movie, score in recommendations:
        st.sidebar.write(f"{movie['title']} - Score: {round(score, 2)}")