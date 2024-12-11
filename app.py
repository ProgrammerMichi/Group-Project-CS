import streamlit as st
#import pandas
#import numpy
#import surprise
#import os
from APIConnection import Instance
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
col1, col2, col3, col4, col5, col6, col7 = st.columns([2,2,2,2,3.2,3,3])

#Checkboxes coming up enable/disable inclusion of respective criteria in the search function
#All inputs (checkboxes and search criteria) are stored in variables, which are later used in the search function
with col1:
    #Dropdown menu with all available genres as options, chosen genre is saved in a variable

    st.write("Genre")
    genrelist = ["None"]
    for i in Instance.get_genres(any):
        genrelist.append(i)
    selgen = st.selectbox("Select Genre", options = genrelist)
    

with col2:
    #Textfield offers option to include an actor during search

    actor_check = st.checkbox("Include Actor")
    selactor = st.text_input("Enter Actor")

    #Option to sort with descending/options ratings
    st.markdown("Order of Ratings")
    selorder = st.selectbox("", ["Descending", "Ascending"])


with col3:
    #First textfield offers option to include a keyword during search
    #second one offers option to exclude a keyword

    keyword_check = st.checkbox("Include Keyword")
    selkeywords = st.text_input("Enter Keyword", key = 1)

    excl_check = st.checkbox("Exclude Keyword")
    exclkeywords = st.text_input("Enter Keyword", key = 2)

with col4:
    
    title_check = st.checkbox("Search by Title")
    seltitle = st.text_input("")
    

with col5:
    #Option to filter according to minimum/maximum rating of movie
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
    #Option to filter according to age rating in Germany, returns movies at or below age rating
    leftleftbox = col6.container(border=True, height = 200)

    ll1, ll2 = leftleftbox.columns(2)
    with ll1:
        st.write("Age Restriction")
    with ll2:
        age_check = st.checkbox ("Apply Restriction")

    selage = leftleftbox.selectbox("", ["FSK 0", "FSK 6", "FSK 12", "FSK 16", "FSK 18"])
       
    
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




if selgen != "None" or actor_check or rating_check or keyword_check or excl_check or rating_check or age_check or length_check and title_check == True:
    st.write("Searching titles only works without any additional criteria selected")
    st.write("Searching by criteria only works without any Title")

if selgen != "None" or actor_check or rating_check or keyword_check or excl_check or rating_check or age_check or length_check and title_check == False:
    #Results of search function stored in variable
    returnmovies = Instance.findmovie(selgen, actor_check, selactor, keyword_check, selkeywords, excl_check, exclkeywords, selorder, rating_check, selmin_rating, selmax_rating, selmin_votes, selmin_length, selmax_length, length_check, age_check, selage)

if returnmovies or returnmovies == {}:
    try:
        returnmovies
    except:
        st.write("") 

    else:

        #Try block tests whether movies have been found
        try:
            for movie in returnmovies:
                movie_id = str(movie["id"])


        #Except block returns string in case the try block fails
        except:
            st.write("No Movies Fitting the Criteria Found")


        #Else block creates for loop which creates a list of movies on the page,
        #including some information and option to rate the movie. 
        #Rating is stored on the site and fed into machine learning system to later be able to make a fitting recommendation
        else: 
            Instance.movielist(returnmovies)

