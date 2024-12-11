import streamlit as st
#import pandas
#import numpy
#import surprise
#import os
from APIConnection import get_genres, findmovie, movielist, search_movie
import pandas as pd
import numpy as np

# Tab Title
st.set_page_config(page_title="Movie Recommender", page_icon="🎞️", layout="wide")

# Title & Intro
st.title("🎞️ Movie Recommender")
st.markdown("**Welcomee to our Movie Recommender!**")
st.markdown("Receive a movie list based on criteria you select, rate the movies and get a recommendation adapted to your likings!")
st.write("")

#Creating columns in order to have criteria options in one row next to each other
col1, col2, col3, col4, col5, col6, col7 = st.columns([2,2,2,2,3.2,3,3])

#Checkboxes coming up take input on whether to enable/disable the respective criteria in the search function
#All inputs (checkboxes and search criteria) are stored in variables, which are later used in the search function


with col1:
    #Dropdown menu with all available genres as options, chosen genre is saved in a variable

    st.write("Genre")
    genrelist = ["None"]
    for i in get_genres(any):
        genrelist.append(i)
    selgen = st.selectbox("Select Genre", options = genrelist)
    

with col2:
    #Textfield takes input on which actor to include during search

    actor_check = st.checkbox("Include Actor")
    selactor = st.text_input("Enter Actor")

    #Input on whether to sort with descending/ascending ratings
    st.markdown("Order of Ratings")
    selorder = st.selectbox("", ["Descending", "Ascending"])


with col3:
    #First textfield takes input (a keyword) to filter for during search
    #second one offers option to exclude a keyword

    keyword_check = st.checkbox("Include Keyword")
    selkeywords = st.text_input("Enter Keyword", key = 1)

    excl_check = st.checkbox("Exclude Keyword")
    exclkeywords = st.text_input("Enter Keyword", key = 2)

with col4:
    #Take input for option to search for movies by title, separate from other filter criteria
    title_check = st.checkbox("Search by Title")
    seltitle = st.text_input("")
    

with col5:
    #Take input for option to filter according to minimum/maximum rating of movie
    #and minimum amount of votes on respective movies

    leftbox = col5.container(border=True, height=275)

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
    

with col6:
    #Take input on which movie ratings in Germany to filter, will return movies at or below age rating
    leftleftbox = col6.container(border=True, height = 200)

    ll1, ll2 = leftleftbox.columns(2)
    with ll1:
        st.write("Age Restriction")
    with ll2:
        age_check = st.checkbox ("Apply Restriction")

    selage = leftleftbox.selectbox("", ["FSK 0", "FSK 6", "FSK 12", "FSK 16", "FSK 18"])
       
    
with col7:
    #Take input on minimum/maximum length of movie

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


#As searching by title and by other criteria are separate, movies of certain criteria only have to be searched for 
#when one isn't searching by title. This ensures that a list such movies will only be returned if search for title is turned off:
if title_check == False:
    returnmovies = findmovie(selgen, actor_check, selactor, keyword_check, selkeywords, excl_check, exclkeywords, selorder, rating_check, selmin_rating, selmax_rating, selmin_votes, selmin_length, selmax_length, length_check, age_check, selage)
    movielist(returnmovies)

#This makes sure that search by title and search by criteria do not interfere with each other and lets the user know if they do:
if selgen == "None":
    selgen = False
conditions = [selgen, actor_check, rating_check, keyword_check, excl_check, rating_check, age_check, length_check]

if any(conditions) and title_check:
    st.write("You can only search for titles without any additional criteria selected")
    st.write("You can only search by criteria without any title")


#List of movies when searching by title:
if not any(conditions) and title_check == True and seltitle:
    movietitle = search_movie(seltitle)
    movielist(movietitle)