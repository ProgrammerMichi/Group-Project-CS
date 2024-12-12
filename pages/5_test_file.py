import requests
import pandas as pd

# Define your TMDB API key
api_key = 'your_tmdb_api_key'

def fetch_movies(endpoint, params, max_pages=5):
    movies = []
    for page in range(1, max_pages + 1):
        params['page'] = page
        response = requests.get(endpoint, params=params)
        data = response.json()
        for movie in data['results']:
            movies.append({
                'title': movie['title'],
                'genres': ', '.join([genre['name'] for genre in movie['genre_ids']]),
                'rating': movie['vote_average'],
                'release_year': movie['release_date'][:4],
                'length': movie.get('runtime', 0)
            })
    return movies

def get_all_movies():
    popular_endpoint = 'https://api.themoviedb.org/3/movie/popular'
    popular_params = {'api_key': api_key, 'language': 'en-US'}
    popular_movies = fetch_movies(popular_endpoint, popular_params)

    top_rated_endpoint = 'https://api.themoviedb.org/3/movie/top_rated'
    top_rated_params = {'api_key': api_key, 'language': 'en-US'}
    top_rated_movies = fetch_movies(top_rated_endpoint, top_rated_params)

    return popular_movies + top_rated_movies

def save_global_ratings_to_csv():
    all_movies = get_all_movies()
    df_global = pd.DataFrame(all_movies)
    df_global.to_csv('global_ratings.csv', index=False)


import streamlit as st
import sqlite3
import authentication
from tmdbv3api import TMDb, Movie, Genre, Discover, Person, Search

authentication.login()

con = sqlite3.connect("userratings.db", check_same_thread=False)
cursor = con.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS userratings (
    ratingId INTEGER PRIMARY KEY AUTOINCREMENT,  
    userId INTEGER,                              
    username TEXT,                               
    movietitle TEXT,                            
    rating REAL                          
)
""")
con.commit()

def get_user_ratings(user_id):
    cursor.execute("SELECT * FROM userratings WHERE userId = ?", (user_id,))
    return cursor.fetchall()

if st.session_state.get("logged_in", False):
    user_ratings = get_user_ratings(st.session_state["userId"])
    if user_ratings:
        st.write("Your Ratings:")
        for rating in user_ratings:
            st.write(rating)
    else:
        st.write("You haven't rated any movies yet.")
else:
    st.write("Log in to view your ratings.")