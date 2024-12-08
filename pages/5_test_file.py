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


Instance = TMDbAPIClient("eb7ed2a4be7573ea9c99867e37d0a4ab")

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=eb7ed2a4be7573ea9c99867e37d0a4ab&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

col0, col1, col2, col3, col4, col5, col6, col7, col8 = st.columns([2,2,2,2,2,2,1,3,3])

with col1:
    genre_check = st.checkbox("Genre")
    if genre_check:
        # This gives a list of movies according to which genre has been picked
        genrelist = ["Select"]
        gl = list(Instance.get_genres(any))
        index = movies[movies['title'] == movie].index[0]
        recommended_movie_names = []
        recommended_movie_posters = []
    for i in gl:
        genrelist.append(i)
        selgen = st.selectbox("Choose Genre", options = genrelist)
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)
        

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


