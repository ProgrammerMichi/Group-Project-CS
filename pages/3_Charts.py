import streamlit as st
import os
import pandas as pd

# Tab Title
st.set_page_config(page_title="Charts", page_icon="📊", layout="wide")
# Title & Intro
st.title("Data Visualisation")
st.write("""hi""")


import requests
import random
import pandas as pd

# TMDB API setup
API_KEY = "eb7ed2a4be7573ea9c99867e37d0a4ab"  # Replace with your TMDb API Key
BASE_URL = "https://api.themoviedb.org/3"
MOVIE_POPULAR_URL = f"{BASE_URL}/movie/popular"
GENRE_URL = f"{BASE_URL}/genre/movie/list"

# Function to fetch genres from TMDb
def fetch_genres():
    params = {
        'api_key': API_KEY,
        'language': 'en-US',
    }
    response = requests.get(GENRE_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        genres = {genre["id"]: genre["name"] for genre in data["genres"]}
        return genres
    else:
        print(f"Error fetching genres: {response.status_code}")
        return {}

# Function to fetch popular movies and include genres
def fetch_popular_movies():
    params = {
        'api_key': API_KEY,
        'language': 'en-US',
        'page': 1  # You can change the page number if you want more results
    }
    
    response = requests.get(MOVIE_POPULAR_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        movies = data.get('results', [])
        return movies
    else:
        print(f"Error fetching movies: {response.status_code}")
        return []

# Fetch genres and popular movies
genres = fetch_genres()
movies = fetch_popular_movies()

# Limit to the first 20 movies (for the sample)
movies = movies[:50]

# Extract necessary movie details (e.g., ID, title, rating, genres)
movie_data = []
for movie in movies:
    genre_names = [genres.get(genre_id) for genre_id in movie.get("genre_ids", [])]
    movie_data.append({
        "movieId": movie["id"],
        "title": movie["title"],
        "rating": movie.get("vote_average", None),  # TMDb movie rating
        "genres": ", ".join(genre_names)  # Concatenate genres into a string
    })

# Create a DataFrame for the movie data
df_movies = pd.DataFrame(movie_data)

# Define sample user data and ratings
user_data = []
user_id = 1  # Single user ID
for index, row in df_movies.iterrows():
    # Randomly assign ratings between 1 and 10
    user_data.append({
        "userId": user_id,  # Only one user
        "movieId": row["movieId"],
        "rating": random.randint(1, 10),  # Random rating between 1 and 10
        "title": row["title"],
        "genres": row["genres"]
    })

# Create a DataFrame for user ratings with movie details
df_ratings = pd.DataFrame(user_data)

# Save the merged data to CSV
RATINGS_FILE = "ratings_with_genres_sample.csv"
df_ratings.to_csv(RATINGS_FILE, index=False)

print(f"Sample data with genres saved to {RATINGS_FILE}")
