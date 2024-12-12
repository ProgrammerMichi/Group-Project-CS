import streamlit as st
import sqlite3
import authentication

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

def get_personal_ratings():
    conn = sqlite3.connect("userratings.db")
    cursor = conn.cursor
    cursor.execute("SELECT * FROM userratings WHERE userId = ?", (st.session_state.get("userId")))
    return cursor.fetchall()


if st.session_state.get("Logged in"):
    get_personal_ratings()