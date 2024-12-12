import sqlite3
import streamlit as st

# Database setup
conn = sqlite3.connect("users.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    userId INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
)
""")
conn.commit()

# Get the next user ID starting from 611
def get_next_user_id():
    cursor.execute("SELECT MAX(userId) FROM users")
    max_id = cursor.fetchone()[0]
    return max_id + 1 if max_id else 611

def register_user(username, password):
    user_id = get_next_user_id()
    cursor.execute("INSERT INTO users (userId, username, password) VALUES (?, ?, ?)", (user_id, username, password))
    conn.commit()

def authenticate_user(username, password):
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    return cursor.fetchone() is not None

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