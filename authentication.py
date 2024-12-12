import sqlite3
import streamlit as st

# Database setup
conn = sqlite3.connect("users.db", check_same_thread=False)
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
    # Validate input
    if not username.strip() or not password.strip():
        st.error("Username and password cannot be empty!")
        return

    try:
        user_id = get_next_user_id()
        cursor.execute("INSERT INTO users (userId, username, password) VALUES (?, ?, ?)", (user_id, username, password))
        conn.commit()
        st.session_state["userId"] = user_id
        st.success("User successfully registered!")
    except sqlite3.IntegrityError as e:
        st.error("Username already exists!")
        st.write(f"Error details: {e}")
    except Exception as e:
        st.error("An error occurred during registration.")
        st.write(f"Error details: {e}")

def authenticate_user(username, password):
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    result = cursor.fetchone()
    if result:
        st.session_state["userId"] = result[0]
        return True
    return False

def initialize_session():
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    if "userId" not in st.session_state:
        st.session_state["userId"] = None
    if "username" not in st.session_state:
        st.session_state["username"] = None

# Streamlit UI
def login():
    # Initialize session state variables
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    if "userId" not in st.session_state:
        st.session_state["userId"] = None
    if "username" not in st.session_state:
        st.session_state["username"] = None

    register = st.sidebar.expander("Register")
    log_in = st.sidebar.expander("Log In")

    with register:
        st.subheader("Register")
        st.write("WARNING: Do NOT use passwords you use elsewhere! This is a course project!")
        new_username = st.text_input("Username", key="register_username")
        new_password = st.text_input("Password", type="password", key="register_password")

        # Only attempt registration if fields are non-empty and the button is clicked
        if st.button("Register"):
            if new_username.strip() and new_password.strip():
                try:
                    register_user(new_username, new_password)
                except sqlite3.IntegrityError:
                    st.error("Username already exists!")
            else:
                st.error("Username and password cannot be empty!")

    with log_in:
        st.subheader("Login")
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")

        if st.button("Login"):
            cursor.execute("SELECT userId FROM users WHERE username = ? AND password = ?", (username, password))
            result = cursor.fetchone()
            if result:
                user_id = result[0]
                st.session_state["logged_in"] = True
                st.session_state["username"] = username
                st.session_state["userId"] = user_id
                st.success(f"Welcome, {username}!")

            else:
                st.error("Invalid username or password.")

    # Session management
    if st.session_state["logged_in"]:
        st.sidebar.write(f"Logged in as: {st.session_state['username']}")
        if st.sidebar.button("Logout"):
            st.session_state["logged_in"] = False
            st.session_state["username"] = None
            st.session_state["userId"] = None
            st.success("Successfully logged out!")

