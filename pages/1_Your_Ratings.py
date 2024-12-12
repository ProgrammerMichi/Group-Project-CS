import streamlit as st
import sqlite3
import authentication
from APIConnectionandRatingDB import load_ratings


# Tab Title, Titles and Intro
st.set_page_config(page_title="Your Ratings", page_icon="📋", layout="wide")
st.title("Your Movie Ratings")
st.write("Here you can find all the movies you have previously rated.")

authentication.login()

# stars for ratings
sentiment_mapping = ["one", "two", "three", "four", "five"]
selected = st.feedback("stars")
if selected is not None:
    st.markdown(f"You selected {sentiment_mapping[selected]} star(s).")


st.write(load_ratings())

if st.session_state.get("logged_in"):
    st.write("Logged in as:", st.session_state.get("username"))

    
