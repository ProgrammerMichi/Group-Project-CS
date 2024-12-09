import streamlit as st
from tmdbv3api import TMDb, Discover, Movie, Genre, Person
from surprise import Dataset, Reader, SVD, accuracy
from surprise.model_selection import train_test_split
import sqlite3
import pandas as pd
import numpy as np
from APIConnection import TMDbAPIClient

# Tab Title
st.set_page_config(page_title="Movie Recommender", page_icon="🎞️", layout="wide")

# Title & Intro
st.title("🎞️ Movie Recommender")

# Verbindung zur TMDb API
Instance = TMDbAPIClient("eb7ed2a4be7573ea9c99867e37d0a4ab")

st.markdown("**hello!**")

# Speicher für Bewertungen und Modell
if "ratings" not in st.session_state:
    st.session_state.ratings = []
if "model" not in st.session_state:
    st.session_state.model = None
if "user_id" not in st.session_state:
    st.session_state.user_id = 1  # Beispiel: Benutzer-ID 1

# SQLite-Datenbank einrichten
conn = sqlite3.connect("movie_recommender.db")
c = conn.cursor()
c.execute("""
CREATE TABLE IF NOT EXISTS ratings (
    user_id INTEGER,
    movie_id INTEGER,
    rating REAL,
    PRIMARY KEY (user_id, movie_id)
)
""")
conn.commit()
conn.close()

# Funktionen für Datenbankoperationen
def save_rating(user_id, movie_id, rating):
    conn = sqlite3.connect("movie_recommender.db")
    c = conn.cursor()
    c.execute("""
    INSERT OR REPLACE INTO ratings (user_id, movie_id, rating) 
    VALUES (?, ?, ?)
    """, (user_id, movie_id, rating))
    conn.commit()
    conn.close()

def get_ratings_by_user(user_id):
    conn = sqlite3.connect("movie_recommender.db")
    c = conn.cursor()
    c.execute("SELECT movie_id, rating FROM ratings WHERE user_id = ?", (user_id,))
    ratings = c.fetchall()
    conn.close()
    return ratings

# Spalten für die Filter
col1, col2, col3, col4, col5, col6, col7, col8 = st.columns([2, 2, 2, 2, 2, 3, 3, 3])

with col1:
    genre_check = st.checkbox("Genre")
    if genre_check:
        genrelist = ["Select"]
        gl = list(Instance.get_genres("movie"))  # Argument "movie" hinzugefügt
        st.write("Geladene Genres:", gl)  # Debugging
        for i in gl:
            genrelist.append(i)
        selgen = st.selectbox("Choose Genre", options=genrelist)

with col2:
    actor_check = st.checkbox("Actor")
    if actor_check:
        selactor = st.text_input("Choose Actor")

with col3:
    keyword_check = st.checkbox("Keywords")
    if keyword_check:
        selkeywords = st.text_input("Enter Keywords")

with col4:
    relate_check = st.checkbox("Similar")

with col5:
    selorder = st.selectbox("Order of Movies by Ratings", ["Descending", "Ascending"])

# Filter für Bewertungen, Länge, Veröffentlichungsdatum
with col6:
    selmin_rating = st.number_input("Minimum Rating", min_value=0.0, max_value=10.0, step=0.1)
    selmax_rating = st.number_input("Maximum Rating", min_value=0.0, max_value=10.0, value=10.0, step=0.1)
    selmin_votes = st.number_input("Minimum Amount of Ratings", min_value=0, value=1000)

with col7:
    selmin_length = st.number_input("Minimum Length (in min)", min_value=0)
    selmax_length = st.number_input("Maximum Length (in min)", min_value=0)

with col8:
    selrel_after = st.date_input("Released After:")
    selrel_before = st.date_input("Released Before:")

## Funktion: Filme finden
def findmovie():
    search_parameters = {}
    if genre_check and selgen != "Select":
        search_parameters["with_genres"] = str(Instance.get_genre_id(selgen))
    if actor_check and selactor:
        selactor_id = Instance.person.search(selactor)
        if selactor_id:  # Überprüfen, ob Ergebnisse für Schauspieler vorliegen
            search_parameters["with_cast"] = str(selactor_id[0].id)
    if keyword_check and selkeywords:
        search_parameters["with_keywords"] = selkeywords.lower()
    if selorder == "Descending":
        search_parameters["sort_by"] = "vote_average.desc"
    else:
        search_parameters["sort_by"] = "vote_average.asc"
    search_parameters["vote_average.gte"] = selmin_rating
    search_parameters["vote_average.lte"] = selmax_rating
    search_parameters["vote_count.gte"] = selmin_votes
    search_parameters["with_runtime.gte"] = selmin_length
    search_parameters["with_runtime.lte"] = selmax_length
    search_parameters["primary_release_date.gte"] = str(selrel_after)
    search_parameters["primary_release_date.lte"] = str(selrel_before)

    # Abrufen der Ergebnisse
    moviesfound = Instance.discover.discover_movies(search_parameters)
    st.write("Suchparameter:", search_parameters)  # Debugging: Zeige die Suchparameter
    st.write("API-Ergebnisse:", moviesfound)      # Debugging: Zeige die API-Rückgabe

    # Sicherstellen, dass "results" im Rückgabewert enthalten ist
    if isinstance(moviesfound, dict) and "results" in moviesfound:
        results = moviesfound.get("results", [])
        if isinstance(results, list):  # Überprüfen, ob es sich um eine Liste handelt
            return results
    return []  # Leere Liste zurückgeben, falls keine Ergebnisse vorhanden sind

# Filme anzeigen und bewerten
if st.button("Suche starten"):
    movies = findmovie()
    st.write("Ergebnisse Typ:", type(movies))  # Debugging
    st.write("Ergebnisse Inhalt:", movies)     # Debugging

    if not movies or len(movies) == 0:
        st.write("Keine Ergebnisse gefunden.")
    else:
        st.write(f"{len(movies)} Ergebnisse gefunden:")
        for movie in movies[:10]:
            if isinstance(movie, dict) and "title" in movie and "vote_average" in movie:
                st.write(f"**{movie['title']}** (Rating: {movie['vote_average']})")
                rating = st.slider(f"Bewertung für '{movie['title']}'", 1, 5, key=f"rate_{movie['id']}")
                if st.button(f"Speichern für '{movie['title']}'", key=f"save_{movie['id']}"):
                    save_rating(st.session_state.user_id, movie["id"], rating)
                    st.write("Bewertung gespeichert!")

# Gespeicherte Bewertungen anzeigen
st.write("Ihre gespeicherten Bewertungen:")
user_ratings = get_ratings_by_user(st.session_state.user_id)
for movie_id, rating in user_ratings:
    st.write(f"Film-ID: {movie_id}, Bewertung: {rating}")

# film bewerten -> wird gespeichert -> passt resultate ah - > 