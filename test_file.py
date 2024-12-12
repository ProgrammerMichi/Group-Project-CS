import streamlit as st
import sqlite3
import authentication
from tmdbv3api import TMDb, Movie, Genre, Discover, Person, Search

authentication.login()

def get_connection():
    return sqlite3.connect("users.db", check_same_thread=False)

con = sqlite3.connect("userratings.db", check_same_thread=False)
cursor = con.cursor()

def get_user_id():
    return st.session_state.get("userId", None)

def save_rating(user_id, username, movietitle, rating):
    cursor.execute("INSERT INTO userratings (userId, username, movietitle, rating) VALUES (?, ?, ?, ?)", 
                    (user_id, username, movietitle, rating))

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

def store_rating(userId, movieId, rating):
    conn = sqlite3.connect("userratings.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS ratings (userId INTEGER, movieId INTEGER, rating REAL)")
    cursor.execute("INSERT INTO ratings (userId, movieId, rating) VALUES (?, ?, ?)", (userId, movieId, rating))
    conn.commit()
    conn.close()
    
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
