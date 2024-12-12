import streamlit as st
import sqlite3
import authentication
from tmdbv3api import TMDb, Movie, Genre, Discover, Person, Search

authentication.login()

con = sqlite3.connect("userratings.db", check_same_thread=False)
cursor = con.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS userratings (
    ratingId INTEGER PRIMARY KEY AUTOINCREMENT,  
    userId INTEGER,                              
    username TEXT,                               
    movietitle TEXT,                            
    rating REAL                          
)
""")
con.commit()

def get_user_ratings(user_id):
    cursor.execute("SELECT * FROM userratings WHERE userId = ?", (user_id,))
    return cursor.fetchall()

if st.session_state.get("logged_in", False):
    user_ratings = get_user_ratings(st.session_state["userId"])
    if user_ratings:
        st.write("Your Ratings:")
        for rating in user_ratings:
            st.write(rating)
    else:
        st.write("You haven't rated any movies yet.")
else:
    st.write("Log in to view your ratings.")