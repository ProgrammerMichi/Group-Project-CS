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

# Tab Title
st.set_page_config(page_title="Movie Recommender", page_icon="🎞️", layout="wide")

# Title & Intro
st.title("🎞️ Movie Recommender")

Instance = TMDbAPIClient("eb7ed2a4be7573ea9c99867e37d0a4ab")

st.markdown("**ho!**")

col1, col2, col3, col4, col5, col6, col7 = st.columns([2,2,2,2,3,3,3])

with col1:
    #This gives a list of movies according to which genre has been picked
    
    st.write("Genre")
    st.write("")
    genrelist = ["Select"]
    gl = list(Instance.get_genres(any))
    for i in gl:
        genrelist.append(i)
    selgen = st.selectbox("Select Genre", options = genrelist)
    

with col2:
    actor_check = st.checkbox("Actor")
    if actor_check:
        selactor = st.text_input("Choose Actor")

with col3:
    keyword_check = st.checkbox("Include Keyword")
    if keyword_check:
        selkeywords = st.text_input("Enter Keyword", key = 1)

    
with col4:
    excl_check = st.checkbox("Exclude Keyword")
    if excl_check:
        exclkeywords = st.text_input("Enter Keyword", key = 2)
    

with col5:
    selorder = st.selectbox("Order of Movies by Ratings", ["Descending", "Ascending"])


with col6:
    leftbox = col6.container(border=True, height=275)

    l1, l2 = leftbox.columns(2)
    with l1:
        st.write ("Ratings")
    with l2:
        rating_check = st.checkbox("Apply Ratings")

    col6_1, col6_2 = leftbox.columns(2)

    with col6_1:
        selmin_rating = st.number_input("Minimum Rating", min_value=0.0, max_value=10.0, step = 0.1, format = "%0.1f")

    with col6_2:
        selmax_rating = st.number_input("Maximum Rating", min_value=0.0, max_value=10.0, value = 10.0, step = 0.1, format = "%0.1f" )

    selmin_votes = leftbox.number_input("Minimum Amount of Ratings", min_value=0, value= 1000)
    
    
    
with col7:
    midbox = col7.container(border=True, height=200)

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


    


 #ChatGPT helped with basic idea of this function(how to manage input that can be turned on/off)   
def findmovie():
    search_parameters = {}
    if selgen != "Select":
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

returnmovies = findmovie()
if returnmovies:
    slidercount = 3
    for movie in returnmovies:
        

        movielisting = st.container(border= True, height = 360)
        lc1, lc2, lc3, lc3_5, lc4, lc5 = movielisting.columns([0.9,1,1,1,1,1])
        movie_id = str(movie["id"])
        details = Instance.get_movie_details(movie_id)

        with lc1:
            try:
                poster_url = Instance.fetch_poster(movie_id)
            except Exception: 
                st.write(st.write("No Poster Available"))
            else:
                st.image(poster_url, caption=movie["title"], use_column_width=True)

                

        with lc2:
            st.write(f"**{details.title}**")
            try:
                description = Instance.fetch_movie_description(movie_id)
            except Exception:
                st.write(st.write("No Description Available"))
            else:
                with st.popover("View Movie Description"):
                    st.write(description)


            
        with lc3:
            st.write("**Actors:**")
            for i in Instance.search_actors(movie_id):
                st.write(i)

        
        with lc4:
            st.write("**Movie Length:**")
            
            length = details.runtime
            mh = str(length // 60)
            mm = str(length % 60)
            st.write(mh,"hours", mm,"min")

            st.text("")
            st.text("")
            st.text("")

            st.write("**Release Date**")
            rd = str(details.release_date)
            st.write(rd) 

        with lc5:
            st.write("**TMDB Movie Rating**")
            st.write(str(round(details.vote_average,1)))

            st.text("")
            st.text("")
            st.text("")
            
            st.slider("**Your Personal Rating**",min_value=1, max_value=10, key = slidercount)
        slidercount += 1