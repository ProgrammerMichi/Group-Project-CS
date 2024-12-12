import streamlit as st
import sqlite3
import authentication
from APIConnectionandRatingDB import load_ratings


# Tab Title, Titles and Intro
st.set_page_config(page_title="Your Ratings", page_icon="📋", layout="wide")
st.title("Your Movie Ratings")
st.write("Here you can find all the movies you have previously rated.")

#Login option
authentication.login()

#Idea was to return a list of all movies the user has rated, with title and rating
st.write(load_ratings())


#Make sure which account you are on
if st.session_state.get("logged_in"):
    st.write("Logged in as:", st.session_state.get("username"))

    
