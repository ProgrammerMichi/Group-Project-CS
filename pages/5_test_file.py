import streamlit as st
from streamlit_option_menu import option_menu
from tmdbv3api import TMDb, Movie, Genre, Discover, Person
#import pandas
#import numpy
#import surprise
#import os
from APIConnection import TMDbAPIClient
import pandas as pd
import numpy as np
import requests  # To make API calls


API_KEY = 'eb7ed2a4be7573ea9c99867e37d0a4ab'
BASE_URL = 'https://api.themoviedb.org/3'


# Function to fetch movies and posters by genre
def fetch_movies_by_genre(genre_id):
    url = f"{BASE_URL}/discover/movie"
    params = {
        "api_key": API_KEY,
        "with_genres": genre_id,
        "sort_by": "popularity.desc",
        "language": "en-US",
        "page": 1,
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return [
            {
                "title": movie["title"],
                "poster_url": f"https://image.tmdb.org/t/p/w500{movie['poster_path']}"
            }
            for movie in data.get("results", [])
            if movie.get("poster_path")  # Ensure the movie has a poster
        ]
    else:
        return []

# Streamlit UI
col0, col1, col2, col3, col4, col5, col6, col7 = st.columns([2,2,2,2,2,2,3,3])
col8, col9, col19, col11, col12 = st.columns(5)

with col1:
    genre_check = st.checkbox("Genre")
    if genre_check:
        # Fetch genres dynamically from TMDb API
        genrelist = [{"id": 0, "name": "Select"}]
        genres = requests.get(f"{BASE_URL}/genre/movie/list", params={"api_key": API_KEY}).json()
        if genres.get("genres"):
            genrelist.extend(genres["genres"])  # Add TMDb genres to the list

        # Display genre selection dropdown
        selgen = st.selectbox("Choose Genre", options=[g["name"] for g in genrelist])

        if selgen != "Select":
            # Get selected genre ID
            selected_genre_id = next(g["id"] for g in genrelist if g["name"] == selgen)

            # Fetch movies and posters for the selected genre
            movies = fetch_movies_by_genre(selected_genre_id)

          # Display movies and poster with st.container():
for movie in movies:
    cols=[col8,col9,coll0,col11,col12]
    for i in range(0,5):
            with cols[i]:
    st.markdown(f"**{movie['title']}**")
    st.image(movie["poster_url"], width=150)



# options to switch pages      
# v1
if st.button("Get started"):
    st.switch_page("app.py")
if st.button("Rate our Recommendations"):
    st.switch_page("pages/1_Ratings.py")
if st.button("See your statistics"):
    st.switch_page("pages/2_Statistics.py")

# v2
app_path = 'https://groupemichi.streamlit.app'
page_file_path = 'pages/Ratings.py'
page = page_file_path.split('/')[1][0:-3]  # get "1_Ratings.py"
st.markdown(
    "Rate our Recommendations " f'''<a href="{app_path}/{page}" target="_self">here</a>''',
    unsafe_allow_html=True)

# v3
url = "https://groupemichi.streamlit.app"
st.write("get started [here](%s)" % url)


