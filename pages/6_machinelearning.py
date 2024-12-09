import streamlit as st
from streamlit_option_menu import option_menu
from tmdbv3api import TMDb, Movie, Genre, Discover, Person
from APIConnection import TMDbAPIClient
import pandas as pd
import numpy as np

# Tab Title
st.set_page_config(page_title="Movie Recommender", page_icon="🎞️", layout="wide")

# Title & Intro
st.title("🎞️ Movie Recommender with Ratings")

# Initialize TMDB API Client
Instance = TMDbAPIClient("eb7ed2a4be7573ea9c99867e37d0a4ab")

# Placeholder for movie ratings
if "user_ratings" not in st.session_state:
    st.session_state["user_ratings"] = {}

# Function to add a rating for a movie
def rate_movie(movie_id, movie_title):
    with st.form(f"rate_movie_form_{movie_id}"):
        st.write(f"Rate '{movie_title}':")
        rating = st.slider("Rating (1-5 stars)", 1, 5, value=3)
        submit = st.form_submit_button("Submit Rating")
        if submit:
            st.session_state["user_ratings"][movie_id] = {
                "title": movie_title,
                "rating": rating,
            }
            st.success(f"Thank you for rating '{movie_title}'!")

# Function to adjust recommendations based on ratings
def adjust_recommendations_with_ratings(movies):
    if not st.session_state["user_ratings"]:
        return movies  # If no ratings exist, return movies as is

    rated_movies = st.session_state["user_ratings"]
    adjusted_movies = []

    for movie in movies:
        similarity_score = 1  # Default similarity score
        for rated_id, details in rated_movies.items():
            if movie["id"] == int(rated_id):
                similarity_score += details["rating"] * 0.2  # Boost for rated movies
        adjusted_movies.append((similarity_score, movie))

    # Sort movies by adjusted score in descending order
    adjusted_movies.sort(key=lambda x: x[0], reverse=True)
    return [movie for _, movie in adjusted_movies]

# Function to find movies based on filters
def find_movies():
    search_parameters = {}
    if genre_check and sel_gen != "Select":
        search_parameters["with_genres"] = str(Instance.get_genre_id(sel_gen))
    if actor_check and sel_actor:
        sel_actor_id = Instance.person.search(sel_actor)
        search_parameters["with_cast"] = str(sel_actor_id[0].id)
    if keyword_check and sel_keywords:
        search_parameters["with_keywords"] = str(sel_keywords.lower())
    if sel_order == "Descending":
        search_parameters["sort_by"] = "vote_average.desc"
    else:
        search_parameters["sort_by"] = "vote_average.asc"
    if rating_check:
        search_parameters["vote_average.gte"] = str(sel_min_rating)
        search_parameters["vote_average.lte"] = str(sel_max_rating)
        search_parameters["vote_count.gte"] = str(sel_min_votes)
    if length_check:
        search_parameters["with_runtime.gte"] = str(sel_min_length)
        search_parameters["with_runtime.lte"] = str(sel_max_length)
    if date_check:
        search_parameters["primary_release_date.gte"] = str(sel_rel_after)
        search_parameters["primary_release_date.lte"] = str(sel_rel_before)

    movies_found = Instance.discover.discover_movies(search_parameters)
    return movies_found

# UI Components
col1, col2, col3, col4, col5, col6, col7, col8 = st.columns([2, 2, 2, 2, 2, 3, 3, 3])

# Genre Selection with Error Handling
with col1:
    genre_check = st.checkbox("Genre")
    if genre_check:
        genre_list = ["Select"]
        try:
            # Passing "movie" as an example argument; replace with the appropriate value if needed
            genres = Instance.get_genres("movie")
            if genres and isinstance(genres, list):
                genre_list += [genre["name"] for genre in genres if "name" in genre]
            else:
                st.error("Could not fetch genres. Please try again later.")
        except Exception as e:
            st.error(f"An error occurred while fetching genres: {e}")
        sel_gen = st.selectbox("Choose Genre", options=genre_list)

with col2:
    actor_check = st.checkbox("Actor")
    if actor_check:
        sel_actor = st.text_input("Choose Actor")

with col3:
    keyword_check = st.checkbox("Keywords")
    if keyword_check:
        sel_keywords = st.text_input("Enter Keywords")

with col4:
    relate_check = st.checkbox("Similar")

with col5:
    sel_order = st.selectbox("Order of Movies by Ratings", ["Descending", "Ascending"])

with col6:
    rating_check = st.checkbox("Apply Ratings")
    sel_min_rating = st.number_input("Minimum Rating", min_value=0.0, max_value=10.0, step=0.1, format="%.1f")
    sel_max_rating = st.number_input("Maximum Rating", min_value=0.0, max_value=10.0, value=10.0, step=0.1, format="%.1f")
    sel_min_votes = st.number_input("Minimum Amount of Ratings", min_value=0, value=1000)

with col7:
    length_check = st.checkbox("Apply Length")
    sel_min_length = st.number_input("Minimum Length (in min)", min_value=0)
    sel_max_length = st.number_input("Maximum Length (in min)", min_value=0)

with col8:
    date_check = st.checkbox("Apply Date")
    sel_rel_after = st.date_input("Released After:")
    sel_rel_before = st.date_input("Released Before:")

# Display Movies and Ratings
return_movies = find_movies()
if return_movies:
    adjusted_movies = adjust_recommendations_with_ratings(return_movies)
    for movie in adjusted_movies:
        st.write(f"🎥 {movie['title']} ({movie['release_date'][:4]})")
        rate_movie(movie["id"], movie["title"])
else:
    st.write("No movies found.")