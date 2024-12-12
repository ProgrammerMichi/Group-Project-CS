import streamlit as st
import pandas as pd
import requests
import random
import plotly.express as px
import plotly.graph_objects as go

# Streamlit setup
st.set_page_config(page_title="Charts", page_icon="📊", layout="wide")
st.title("Data Visualisation")
st.write("...")

# TMDB API setup
API_KEY = "eb7ed2a4be7573ea9c99867e37d0a4ab"
BASE_URL = "https://api.themoviedb.org/3"
MOVIE_POPULAR_URL = f"{BASE_URL}/movie/popular"
GENRE_URL = f"{BASE_URL}/genre/movie/list"
MOVIE_DETAILS_URL = f"{BASE_URL}/movie"

# Fetch genres from TMDb
def fetch_genres():
    response = requests.get(GENRE_URL, params={'api_key': API_KEY, 'language': 'en-US'})
    if response.status_code == 200:
        return {genre["id"]: genre["name"] for genre in response.json().get("genres", [])}
    print(f"Error fetching genres: {response.status_code}")
    return {}

# Fetch movie details (length and release year)
def fetch_movie_details(movie_id):
    response = requests.get(f"{MOVIE_DETAILS_URL}/{movie_id}", params={'api_key': API_KEY, 'language': 'en-US'})
    if response.status_code == 200:
        data = response.json()
        return data.get("runtime"), data.get("release_date", "")[:4]
    print(f"Error fetching movie details for ID {movie_id}: {response.status_code}")
    return None, None

# Fetch popular movies with details
def fetch_popular_movies(pages=10):
    movies = []
    for page in range(1, pages + 1):
        response = requests.get(MOVIE_POPULAR_URL, params={'api_key': API_KEY, 'language': 'en-US', 'page': page})
        if response.status_code == 200:
            movies.extend(response.json().get('results', []))
        else:
            print(f"Error fetching movies: {response.status_code}")
    return movies

# Process movies and genres
genres = fetch_genres()
movies = fetch_popular_movies(pages=3)[:100]
movie_data = []
for movie in movies:
    runtime, release_year = fetch_movie_details(movie["id"])
    if release_year and int(release_year) <= 2024:
        movie_data.append({
        "movieId": movie["id"],
        "title": movie["title"],
        "rating": movie.get("vote_average"),
        "genres": ", ".join(genres.get(genre_id) for genre_id in movie.get("genre_ids", [])),
        "length": runtime,
        "release_year": release_year
    })

# Create DataFrame
df_movies = pd.DataFrame(movie_data)

# Generate random user ratings
df_ratings = pd.DataFrame([{
    "userId": 1,
    "movieId": row["movieId"],
    "rating": random.randint(1, 10),
    "title": row["title"],
    "genres": row["genres"],
    "length": row["length"],
    "release_year": row["release_year"]
} for _, row in df_movies.iterrows()])

# Save to CSV and display in Streamlit
RATINGS_FILE = "ratings_with_genres_and_details_sample.csv"
df_ratings.to_csv(RATINGS_FILE, index=False)
print(f"Sample data with genres and details saved to {RATINGS_FILE}")

st.title("Movie Ratings with Genres and Details")
st.dataframe(df_ratings)




# Define your TMDB API key and endpoint
api_key = 'your_tmdb_api_key'
endpoint = 'https://api.themoviedb.org/3/movie/popular'

# Fetch data from TMDB API
params = {'api_key': api_key, 'language': 'en-US', 'page': 1}
response = requests.get(endpoint, params=params)
data = response.json()

# Extract relevant data
movies = [{
    'title': movie['title'],
    'genres': ', '.join([genre['name'] for genre in movie['genre_ids']]),
    'rating': movie['vote_average'],
    'release_year': movie['release_date'][:4],  # Extract year from release date
    'length': movie.get('runtime', 0)  # Default to 0 if runtime is not available
} for movie in data['results']]

# Create a DataFrame and save to CSV
RATINGS_FILE = "global_ratings.csv"
df_global = pd.DataFrame(movies)
df_global.to_csv('global_ratings.csv', index=False)

# Display the DataFrame
st.dataframe(df_global)
