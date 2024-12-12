import sqlite3
import streamlit as st

# Database setup
conn = sqlite3.connect("users.db")
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS users")
conn.commit()
