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
    username = st.session_state.get("username")
    st.write(username)
    if not username:
        return "No username found. Please log in to view your ratings."
    
    conn = sqlite3.connect("userratings.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM userratings WHERE username = ?", (username,))
    ratings = cursor.fetchall()
    conn.close()
    return ratings


if st.session_state.get("logged_in"):
    st.write("Logged in as:", st.session_state.get("username"))
    st.write("User ID:", st.session_state.get("userID"))
    
if st.session_state.get("logged_in"):
    user_ratings = get_personal_ratings()
    if isinstance(user_ratings, str):  # Handle error messages
        st.write(user_ratings)
    elif user_ratings:
        st.write("Your Ratings:")
        for rating in user_ratings:
            st.write(rating)
    else:
        st.write("You haven't rated any movies yet.")