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

# File paths
USERS_FILE = "users.csv"
RATINGS_FILE = "user_ratings.csv"

# Initialize user database if not exists
if not os.path.exists(USERS_FILE):
    pd.DataFrame(columns=["username", "password"]).to_csv(USERS_FILE, index=False)

# Initialize session state variables
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "current_user" not in st.session_state:
    st.session_state.current_user = None
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "user_ratings" not in st.session_state:
    if os.path.exists(RATINGS_FILE):
        st.session_state.user_ratings = pd.read_csv(RATINGS_FILE)
    else:
        st.session_state.user_ratings = pd.DataFrame(columns=["userId", "movieId", "rating"])

# Authentication functions
def authenticate_user(username, password):
    users = pd.read_csv(USERS_FILE)
    user = users[(users["username"] == username) & (users["password"] == password)]
    return not user.empty

def register_user(username, password):
    users = pd.read_csv(USERS_FILE)
    if username in users["username"].values:
        return False  # User already exists
    new_user = pd.DataFrame({"username": [username], "password": [password]})
    updated_users = pd.concat([users, new_user], ignore_index=True)
    updated_users.to_csv(USERS_FILE, index=False)
    return True

# Sidebar for login/registration
st.sidebar.title("User Login")
if not st.session_state.logged_in:
    auth_action = st.sidebar.selectbox("Action", ["Login", "Register"])

    if auth_action == "Login":
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password", type="password")
        if st.sidebar.button("Login"):
            if authenticate_user(username, password):
                st.sidebar.success(f"Welcome back, {username}!")
                st.session_state.logged_in = True
                st.session_state.current_user = username
                st.session_state.user_id = (
                    pd.read_csv(USERS_FILE)
                    .loc[pd.read_csv(USERS_FILE)["username"] == username]
                    .index[0]
                    + 1
                )  # User ID is the row index + 1
            else:
                st.sidebar.error("Invalid credentials!")
    elif auth_action == "Register":
        username = st.sidebar.text_input("New Username")
        password = st.sidebar.text_input("New Password", type="password")
        if st.sidebar.button("Register"):
            if register_user(username, password):
                st.sidebar.success("Registration successful! Please log in.")
            else:
                st.sidebar.error("Username already exists!")
else:
    st.sidebar.success(f"Logged in as {st.session_state.current_user}")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.current_user = None
        st.session_state.user_id = None
        st.stop()

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
                new_rating = pd.DataFrame({"userId": [st.session_state.user_id], "movieId": [movie_id], "rating": [rating]})
                st.session_state.user_ratings = pd.concat([st.session_state.user_ratings, new_rating], ignore_index=True)
                st.session_state.user_ratings.to_csv(RATINGS_FILE, index=False)
                st.success(f"Rating saved for {movie['title']}!")

# Display recommendations
if st.sidebar.button("Get Recommendations"):
    recommendations = []
    for movie in returnmovies:
        score = calculate_score(movie, st.session_state.user_id, st.session_state.user_ratings)
        recommendations.append((movie, score))

    # Sort recommendations by score
    recommendations = sorted(recommendations, key=lambda x: x[1], reverse=True)[:5]

    st.sidebar.markdown("### Recommended Movies:")
    for movie, score in recommendations:
        st.sidebar.write(f"{movie['title']} - Score: {round(score, 2)}")