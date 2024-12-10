import streamlit as st
from tmdbv3api import TMDb, Movie, Genre, Discover, Person
from APIConnection import TMDbAPIClient
import pandas as pd
import numpy as np
import os

# Tab Title & Layout
st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎞️",
    layout="wide",
)

# Title & Intro
st.title("🎞️ Movie Recommender")
st.markdown("**Welcome to your personalized movie recommender!**")

# Load API Key and User ID
API_KEY = "YOUR_TMDB_API_KEY"  # Replace with your actual API key
USER_ID = 1

# Initialize TMDb Client and User Ratings
tmdb = TMDb(API_KEY)
ratings_file = "user_ratings.csv"
if os.path.exists(ratings_file):
    user_ratings = pd.read_csv(ratings_file)
else:
    user_ratings = pd.DataFrame(columns=["userId", "movieId", "rating"])

# Navigation Bar
st.sidebar.header("Filters")

# Filter Options with Collapsible Sections
with st.expander("**Genre**"):
    genre_list = ["Select"] + [genre.get("name") for genre in tmdb.genres().get("genres")]
    selected_genre = st.selectbox("Choose Genre", options=genre_list)

with st.expander("**Actors**"):
    selected_actor = st.text_input("Enter Actor Name")

with st.expander("**Keywords**"):
    include_keywords = st.text_input("Include Keywords (Separate by commas)")
    exclude_keywords = st.text_input("Exclude Keywords (Separate by commas)")

with st.expander("**Rating**"):
    order_by_rating = st.selectbox("Order Movies By", ["Descending", "Ascending"])
    min_rating = st.number_input("Minimum Rating", min_value=0.0, max_value=10.0, step=0.1, format="%0.1f")
    max_rating = st.number_input("Maximum Rating", min_value=0.0, max_value=10.0, value=10.0, step=0.1, format="%0.1f")
    min_votes = st.number_input("Minimum Amount of Ratings", min_value=0)

with st.expander("**Length**"):
    min_length = st.number_input("Minimum Length (in min)", min_value=0)
    max_length = st.number_input("Maximum Length (in min)", min_value=0)

with st.expander("**Restrictions**"):
    exclude_adult = st.checkbox("Exclude Adult Movies")

# Function to fetch movies based on filters
def find_movies():
    search_params = {}
    if selected_genre != "Select":
        genre_id = tmdb.genres().get_genre_id(selected_genre)
        search_params["with_genres"] = str(genre_id)
    if selected_actor:
        actor_results = tmdb.search().person(selected_actor)
        if actor_results.total_results > 0:
            search_params["with_cast"] = str(actor_results.results[0].id)
    if include_keywords:
        keywords = ",".join([str(tmdb.keywords().get_keyword_id(keyword)) for keyword in include_keywords.split(",")])
        search_params["with_keywords"] = keywords
    if exclude_keywords:
        keywords = ",".join([str(tmdb.keywords().get_keyword_id(keyword)) for keyword in exclude_keywords.split(",")])
        search_params["without_keywords"] = keywords
    if order_by_rating == "Descending":
        search_params["sort_by"] = "vote_average.desc"
    else:
        search_params["sort_by"] = "vote_average.asc"

    search_params["vote_average.gte"] = str(min_rating)
    search_params["vote_average.lte"] = str(max_rating)
    search_params["vote_count.gte"] = str(min_votes)

    search_params["with_runtime.gte"] = str(min_length)
    search_params["with_runtime.lte"] = str(max_length)

    if exclude_adult:
        search_params["include_adult"] = "false"

    return tmdb.discover.movie(search_params)

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
        [m["id"] for m in return_movies if set(genre_ids).intersection(m.get("genre_ids", []))]
    )]
    return similar_movies["movieId"].tolist()

# Find movies based on filters
return_movies = find_movies()

# Allow users to rate movies
if return_movies:
    for movie in return_movies:
        movie_listing = st.container()
        lc1, lc2, lc3 = movie_listing.columns([1.3, 3, 2])
        movie_id = movie["id"]

        with lc1:
            try:
                poster_url = tmdb.images().get_poster_path(movie_id)
                st.image(poster_url, caption=movie["title"], use_column_width=True)
            except:
                st.write("No Poster Available")

        with lc2:
            st.write(f"**{movie['title']}**")
            st.write(f"TMDB Rating: {movie.get('vote_average', 'N/A')}")

        with lc3:
            rating = st.slider(f"Rate {movie['title']}", 1, 10, key=f"slider_{movie_id}")
            if st.button(f"Save Rating for {movie['title']}", key=f"button_{movie_id}"):
                new_rating = pd.DataFrame({"userId": [USER_ID], "movieId": [movie_id], "rating": [rating]})
                user_ratings = pd.concat([user_ratings, new_rating], ignore_index=True)
                user_ratings.to_csv(ratings_file, index=False)  # Save ratings to CSV
                st.success(f"Rating saved for {movie['title']}")

# Display recommendations
if st.sidebar.button("Get Recommendations"):
    recommendations = []
    for movie in return_movies:
        score = calculate_score(movie, USER_ID, user_ratings)
        recommendations.append((movie, score))

    # Sort recommendations by score
    recommendations = sorted(recommendations, key=lambda x: x[1], reverse=True)[:5]

    st.sidebar.markdown("### Recommended Movies:")
    for movie, score in recommendations:
        st.sidebar.write(f"{movie['title']} - Score: {round(score, 2)}")