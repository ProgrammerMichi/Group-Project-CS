import streamlit as st
import pandas as pd
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# --- TMDb API Key ---
API_KEY = "DEIN_API_KEY_HIER"

# --- Funktion zum Laden von Daten aus TMDb ---
@st.cache
def load_movies(query):
    url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={query}"
    response = requests.get(url).json()
    return response.get('results', [])

# --- Funktion zum Abrufen der Film-Details ---
def get_movie_details(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"
    response = requests.get(url).json()
    return response

# --- Funktion für Content-Based Recommendation ---
def recommend_movies(selected_movie, movie_list):
    if not selected_movie:
        return []
    
    # Erstelle einen DataFrame aus den Film-Beschreibungen
    movies_df = pd.DataFrame(movie_list)
    movies_df['overview'] = movies_df['overview'].fillna("")

    # Vektorisierung der Beschreibungen
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(movies_df['overview'])

    # Berechnung der Cosine Similarity
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    # Index des ausgewählten Films
    selected_index = movies_df[movies_df['title'] == selected_movie].index[0]
    similarity_scores = list(enumerate(cosine_sim[selected_index]))
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)

    # Rückgabe der Top 5 ähnlichen Filme
    top_movies_indices = [i[0] for i in similarity_scores[1:6]]
    return movies_df.iloc[top_movies_indices]

# --- Streamlit Benutzeroberfläche ---
st.title("🎥 Filmempfehlungs-App")
st.sidebar.header("Sucheinstellungen")

# Eingabe des Nutzers
user_query = st.sidebar.text_input("Gib einen Filmtitel ein:")
selected_genre = st.sidebar.selectbox("Genre", ["Alle", "Action", "Drama", "Komödie", "Thriller"])

# Filmliste laden
if user_query:
    movie_list = load_movies(user_query)

    if movie_list:
        # Anzeige der Suchergebnisse
        st.subheader("Suchergebnisse")
        for movie in movie_list:
            st.write(f"**{movie['title']}** ({movie['release_date'][:4] if movie.get('release_date') else 'N/A'})")
            st.write(movie['overview'])
            if movie.get('poster_path'):
                st.image(f"https://image.tmdb.org/t/p/w500{movie['poster_path']}", width=150)

        # Auswahl eines Films für Empfehlungen
        selected_movie = st.selectbox("Wähle einen Film für Empfehlungen", [m['title'] for m in movie_list])

        if selected_movie:
            # Empfehlungen basierend auf dem ausgewählten Film
            st.subheader(f"Empfehlungen basierend auf {selected_movie}")
            recommendations = recommend_movies(selected_movie, movie_list)

            if not recommendations.empty:
                for _, rec_movie in recommendations.iterrows():
                    details = get_movie_details(rec_movie['id'])
                    st.write(f"**{rec_movie['title']}**")
                    st.write(rec_movie['overview'])
                    if details.get('poster_path'):
                        st.image(f"https://image.tmdb.org/t/p/w500{details['poster_path']}", width=150)
            else:
                st.write("Keine Empfehlungen gefunden. Probiere eine andere Auswahl.")
    else:
        st.write("Keine Filme gefunden. Versuche einen anderen Suchbegriff.")
else:
    st.write("Gib einen Filmtitel ein, um zu beginnen!")
