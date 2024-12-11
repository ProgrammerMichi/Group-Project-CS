import streamlit as st
#import pandas
#import numpy
#import surprise
#import os
from APIConnection import Instance
from SearchFilters import findmovie
import pandas as pd
import numpy as np

# Tab Title
st.set_page_config(page_title="Movie Recommender", page_icon="🎞️", layout="wide")

# Title & Intro
st.title("🎞️ Movie Recommender")
st.markdown("**Welcome to our Movie Recommender!**")
st.markdown("Receive a movie list based on criteria you select, rate the movies and get a recommendation adapted to your likings!")
st.write("")

#Creating columns in order to have criteria options in one row next to each other
col1, col2, col3, col4, col5, col6, col7 = st.columns([2,2,2,2,3,3,3])

#Checkboxes coming up enable/disable inclusion of respective criteria in the search function
#All variables (checkboxes and those of search criteria) are stored in variables, which are later used in the search function
with col1:
    #Dropdown menu with all available genres as options, chosen genre is saved in a variable

    st.write("Genre")
    genrelist = ["None"]
    gl = list(Instance.get_genres(any))
    for i in gl:
        genrelist.append(i)
    selgen = st.selectbox("Select Genre", options = genrelist)
    

with col2:
    #Textfield offers option to include an actor in search, 

    actor_check = st.checkbox("Include Actor")
    selactor = st.text_input("Enter Actor")


with col3:
    #Textfield offers option to include a keyword in search,

    keyword_check = st.checkbox("Include Keyword")
    selkeywords = st.text_input("Enter Keyword", key = 1)


with col4:
    #Textfield offers option to include a keyword in search,

    excl_check = st.checkbox("Exclude Keyword")
    exclkeywords = st.text_input("Enter Keyword", key = 2)
    

with col5:
    #Option to sort with descending/options ratings

    st.markdown("Order of Movies by Ratings")
    selorder = st.selectbox("", ["Descending", "Ascending"])


with col6:
    #Option to filter according to minimum/maximum rating of movie
    #and minimum amount of votes on respective movies

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
    #Option to filter according to minimum/maximum length of movie

    rightbox = col7.container(border=True, height=200)

    m1, m2 = rightbox.columns(2)
    with m1:
        st.write("Length")
    with m2:
        length_check = st.checkbox("Apply Length")

    col7_1, col7_2 = rightbox.columns(2)

    with col7_1:
        selmin_length = st.number_input("Minimum Length (in min)", min_value=0)

    with col7_2:
        selmax_length = st.number_input("Maximum Length (in min)", min_value=0)


#Results of search function stored in variable

returnmovies = findmovie(selgen, actor_check, selactor, keyword_check, selkeywords, excl_check, exclkeywords, selorder, rating_check, selmin_rating, selmax_rating, selmin_votes, selmin_length, selmax_length, length_check)


#Try function tests whether movies have been found
try:
    for movie in returnmovies:
        movie_id = str(movie["id"])


#Except function returns that no movies where found in case the try function fails
except:
    st.write("No Movies Fitting the Criteria Found")


#Else function creates for loop which creates a list of containers on the site,
#including some information and option to rate the movie. 
#Rating is stored on the site and fed into machine learning system to later be able to make a fitting recommendation
else: 
    slidercount = 3
    for movie in returnmovies:
        
        movielisting = st.container(border= True, height = 360)
        lc1, lc2, lc3, lc3_5, lc4, lc5 = movielisting.columns([0.85,1,1,0.8,1,1])
        movie_id = str(movie["id"])
        details = Instance.get_movie_details(movie_id)

        with lc1:
            try:
                poster_url = Instance.fetch_poster(movie_id)
            except Exception: 
                st.write(st.write("No Poster Available"))
            else:
                st.image(poster_url, caption=movie["title"])

                

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
            st.write("**Lead Actors:**")
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