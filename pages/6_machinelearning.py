import streamlit as st
from streamlit_option_menu import option_menu
from tmdbv3api import TMDb, Movie, Genre, Discover, Person
from APIConnection import TMDbAPIClient
import pandas as pd
import numpy as np

# Tab Title
st.set_page_config(page_title="Movie Recommender", page_icon="🎞️", layout="wide")

# Title & Intro
st.title("🎞️ Movie Recommender")

Instance = TMDbAPIClient("eb7ed2a4be7573ea9c99867e37d0a4ab")

st.markdown("**hello!**")

# Initialize user ratings storage
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

# Recommendation function based on user ratings
def recommend_movies(user_id, movies, ratings_df, top_n=5):
    if ratings_df.empty:
        return []
    rated_movies = ratings_df[ratings_df["userId"] == user_id]
    avg_rating = rated_movies["rating"].mean()

    recommendations = []
    for movie in movies:
        movie_id = movie["id"]
        if movie_id not in rated_movies["movieId"].values:
            movie_rating = movie.get("vote_average", 0)
            score = (avg_rating + movie_rating) / 2
            recommendations.append((movie, score))

    recommendations.sort(key=lambda x: x[1], reverse=True)
    return recommendations[:top_n]

returnmovies = findmovie()

if returnmovies:
    for movie in returnmovies:
        movielisting = st.container()
        lc1, lc2, lc3, lc4, lc5 = movielisting.columns([1.3, 1.5, 3.1, 2, 2])
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

        with lc5:
            # Use the unique movie_id as part of the key
            rating = st.slider(f"Rate {movie['title']}", 1, 10, key=f"slider_{movie_id}")
            if st.button(f"Save Rating for {movie['title']}", key=f"button_{movie_id}"):
                new_rating = pd.DataFrame({"userId": [1], "movieId": [movie_id], "rating": [rating]})
                user_ratings = pd.concat([user_ratings, new_rating], ignore_index=True)
                st.success(f"Rating saved for {movie['title']}")

# Display recommendations
if st.sidebar.button("Get Recommendations"):
    recommendations = recommend_movies(1, returnmovies, user_ratings)
    st.sidebar.markdown("### Recommended Movies:")
    for movie, score in recommendations:
        st.sidebar.write(f"{movie['title']} - Predicted Score: {round(score, 2)}")