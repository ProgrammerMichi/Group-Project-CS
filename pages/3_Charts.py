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
def fetch_popular_movies(pages=3):
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
movies = fetch_popular_movies(pages=3)[:50]
movie_data = []
for movie in movies:
    runtime, release_year = fetch_movie_details(movie["id"])
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


# Distribution of Movie Ratings
fig1 = px.histogram(df_ratings, x="rating", nbins=10, title="Distribution of Movie Ratings")
fig1.show()

# Average Rating by Genre
# Split genres into multiple rows
df_genres = df_ratings.assign(genres=df_ratings['genres'].str.split(', ')).explode('genres')
avg_rating_by_genre = df_genres.groupby('genres')['rating'].mean().reset_index()
fig2 = px.bar(avg_rating_by_genre, x="genres", y="rating", title="Average Rating by Genre")
fig2.show()


# Number of Movies by Release Year
movies_by_year = df_ratings.groupby('release_year').size().reset_index(name='count')
fig4 = px.bar(movies_by_year, x="release_year", y="count", title="Number of Movies by Release Year")
fig4.show()


# Pie chart with genres
df_genres = df_ratings.assign(genres=df_ratings['genres'].str.split(', ')).explode('genres')
genre_counts = df_genres['genres'].value_counts().reset_index()
genre_counts.columns = ['genres', 'count']
fig5 = px.pie(genre_counts, names='genres', values='count', title='Distribution of Genres')
fig5.show()

# Radar chart for similarities (example using average rating by genre)
genre_ratings = df_genres.groupby('genres')['rating'].mean().reset_index()
fig6 = go.Figure()
fig6.add_trace(go.Scatterpolar(
    r=genre_ratings['rating'],
    theta=genre_ratings['genres'],
    fill='toself'
))
fig6.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[0, 10]
        )),
    showlegend=False,
    title='Radar Chart for Average Ratings by Genre'
)
fig6.show()

# Total movie runtime for each genre
genre_runtime = df_genres.groupby('genres')['length'].sum().reset_index()
fig7 = px.bar(genre_runtime, x='genres', y='length', title='Total Movie Runtime for Each Genre')
fig7.show()