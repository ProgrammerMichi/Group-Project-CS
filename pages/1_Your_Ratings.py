import streamlit as st
import sqlite3
import authentication
import os
import json

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

# File path for ratings.json
RATINGS_FILE = os.path.join(os.path.dirname(__file__), "ratings.json")

# Load ratings from JSON file
def load_ratings():
    if not os.path.exists(RATINGS_FILE):
        return {}
    with open(RATINGS_FILE, "r") as file:
        return json.load(file)

# Save ratings to JSON file
def save_ratings(ratings):
    with open(RATINGS_FILE, "w") as file:
        json.dump(ratings, file, indent=4)

# Add or update a user's rating for a movie
def add_rating(username, movie, rating):
    ratings = load_ratings()
    if username not in ratings:
        ratings[username] = {}
    ratings[username][movie] = rating
    save_ratings(ratings)


if st.session_state.get("logged_in"):
    st.write("Logged in as:", st.session_state.get("username"))

    
