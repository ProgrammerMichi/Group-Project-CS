import sqlite3
import streamlit as st

# Database setup
conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()

# Create tables if they don't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    userId INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS userratings (
    ratingId INTEGER PRIMARY KEY AUTOINCREMENT,
    userId INTEGER,
    username TEXT,
    movietitle TEXT,
    rating REAL
)
""")
conn.commit()

# Initialize session state variables
if "userID" not in st.session_state:
    st.session_state["userID"] = None

# Get the next user ID starting from 611
def get_next_user_id():
    cursor.execute("SELECT MAX(userId) FROM users")
    max_id = cursor.fetchone()[0]
    return max_id + 1 if max_id else 611

# Register a user
def register_user(username, password):
    user_id = get_next_user_id()
    cursor.execute("INSERT INTO users (userId, username, password) VALUES (?, ?, ?)", (user_id, username, password))
    conn.commit()
    st.session_state["userID"] = user_id

# Authenticate a user
def authenticate_user(username, password):
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    return cursor.fetchone() is not None

# Save a movie rating
def save_rating(user_id, username, movietitle, rating):
    cursor.execute("INSERT INTO userratings (userId, username, movietitle, rating) VALUES (?, ?, ?, ?)", 
                   (user_id, username, movietitle, rating))
    conn.commit()

# Retrieve ratings for the logged-in user
def get_personal_ratings(user_id):
    cursor.execute("SELECT movietitle, rating FROM userratings WHERE userId = ?", (user_id,))
    return cursor.fetchall()

# Streamlit UI
def login():
    register = st.sidebar.expander("Register")
    log_in = st.sidebar.expander("Log In")

    with register:
        st.subheader("Register")
        st.write("WARNING: Do NOT use passwords you use elsewhere! This is a course project!")
        new_username = st.text_input("Username", key="register_username")
        new_password = st.text_input("Password", type="password", key="register_password")

        if st.button("Register"):
            try:
                register_user(new_username, new_password)
                st.success("User successfully registered! Please log in.")
            except sqlite3.IntegrityError:
                st.error("Username already exists!")

    with log_in:
        st.subheader("Login")
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")

        if st.button("Login"):
            if authenticate_user(username, password):
                st.success(f"Welcome, {username}!")
                st.session_state["logged_in"] = True
                st.session_state["username"] = username

                # Retrieve and display personal ratings
                user_id = st.session_state["userID"]
                user_ratings = get_personal_ratings(user_id)
                if user_ratings:
                    st.write("Your Ratings:")
                    for movie, rating in user_ratings:
                        st.write(f"{movie}: {rating}")
                else:
                    st.write("You haven't rated any movies yet.")

            else:
                st.error("Invalid username or password.")

    # Session management
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if st.session_state["logged_in"]:
        st.sidebar.write(f"Logged in as: {st.session_state['username']}")
        if st.sidebar.button("Logout"):
            st.session_state["logged_in"] = False
            st.session_state["username"] = None
            st.success("Successfully logged out!")

# Main
login()

