import streamlit as st
import sqlite3
import authentication
from APIConnectionandRatingDB import load_ratings, get_user_movie_ratings


# Tab Title, Titles and Intro
st.set_page_config(page_title="Ratings", page_icon="📋", layout="wide")
st.title("Your Movie Ratings")
st.write("Here you can find all the movies you have previously rated.")

authentication.login()

# stars for ratings
sentiment_mapping = ["one", "two", "three", "four", "five"]
selected = st.feedback("stars")
if selected is not None:
    st.markdown(f"You selected {sentiment_mapping[selected]} star(s).")

if "logged_in" in st.session_state and st.session_state["logged_in"]:
    movie_rating_list = get_user_movie_ratings()
    if movie_rating_list:
        for movie_rating in movie_rating_list:
            st.write(movie_rating)
    else:
        st.write("You haven't rated any movies yet.")
else:
    st.warning("Please log in to see your rated movies.")

if st.session_state.get("logged_in"):
    st.write("Logged in as:", st.session_state.get("username"))

    
