#kombinierter Code Schritte 1-4
import streamlit as st
import pandas as pd
from tmdbv3api import TMDb, Discover
from surprise import Dataset, Reader, SVD, accuracy
from surprise.model_selection import train_test_split

# Verbindung zur TMDb API
Instance = TMDb("eb7ed2a4be7573ea9c99867e37d0a4ab")

# Streamlit-Seiteneinstellungen
st.set_page_config(page_title="Movie Recommender", page_icon="🎞️", layout="wide")
st.title("🎞️ Movie Recommender - Alle Schritte")

# Speicher für Bewertungen
if "ratings" not in st.session_state:
    st.session_state.ratings = []
if "model" not in st.session_state:
    st.session_state.model = None

# Schritt 1: Filme anzeigen und bewerten
def find_movies():
    return Instance.discover.discover_movies({"sort_by": "popularity.desc"})

movies = find_movies()
if movies:
    st.write("Bitte bewerten Sie die folgenden Filme:")
    for movie in movies[:10]:  # Zeige nur die ersten 10 Filme
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"**{movie['title']}** (Rating: {movie['vote_average']})")
        with col2:
            rating = st.radio(f"Bewertung für '{movie['title']}'", options=[1, 2, 3, 4, 5], key=f"rate_{movie['id']}")
            if rating:
                st.session_state.ratings.append({"user_id": 1, "movie_id": movie["id"], "rating": rating})

# Schritt 2: Daten vorbereiten
if st.button("Daten vorbereiten"):
    if not st.session_state.ratings:
        st.write("Es wurden noch keine Bewertungen abgegeben. Bitte bewerten Sie zuerst einige Filme!")
    else:
        ratings_df = pd.DataFrame(st.session_state.ratings)
        st.write("Gesammelte Bewertungen:")
        st.write(ratings_df)

        # Daten für Surprise vorbereiten
        reader = Reader(rating_scale=(1, 5))
        data = Dataset.load_from_df(ratings_df[["user_id", "movie_id", "rating"]], reader)
        st.write("Daten sind bereit für das Training!")

# Schritt 3: Modelltraining
if st.button("Modell trainieren"):
    if not st.session_state.ratings:
        st.write("Es wurden noch keine Bewertungen abgegeben. Bitte bewerten Sie zuerst einige Filme!")
    else:
        ratings_df = pd.DataFrame(st.session_state.ratings)
        reader = Reader(rating_scale=(1, 5))
        data = Dataset.load_from_df(ratings_df[["user_id", "movie_id", "rating"]], reader)
        trainset, testset = train_test_split(data, test_size=0.2)

        model = SVD()
        model.fit(trainset)

        predictions = model.test(testset)
        rmse = accuracy.rmse(predictions)
        st.write(f"Das Modell wurde trainiert. RMSE: {rmse:.2f}")
        st.session_state.model = model
        st.write("Das Modell wurde gespeichert und kann für Empfehlungen verwendet werden.")

# Schritt 4: Empfehlungen anzeigen
if st.button("Empfehlungen anzeigen"):
    if "model" not in st.session_state:
        st.write("Bitte trainiere zuerst das Modell!")
    else:
        st.write("Empfehlungen basierend auf Ihren Bewertungen:")

        all_movie_ids = [movie["id"] for movie in movies]
        predictions = []
        for movie_id in all_movie_ids:
            pred = st.session_state.model.predict(uid=1, iid=movie_id)
            predictions.append((movie_id, pred.est))

        predictions.sort(key=lambda x: x[1], reverse=True)
        for movie_id, pred_rating in predictions[:5]:
            movie = next((m for m in movies if m["id"] == movie_id), None)
            if movie:
                st.write(f"**{movie['title']}** (Vorhergesagte Bewertung: {pred_rating:.2f})")
