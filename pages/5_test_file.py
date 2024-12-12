import requests
import pandas as pd
import streamlit as st

# Define your TMDB API key and endpoint
api_key = 'eb7ed2a4be7573ea9c99867e37d0a4ab'
endpoint = 'https://api.themoviedb.org/3/movie/popular'

# Fetch data from TMDB API
params = {
    'api_key': api_key,
    'language': 'en-US',
    'page': 1  # You can loop through multiple pages if needed
}
response = requests.get(endpoint, params=params)
data = response.json()


# Extract relevant data
movies = []
for movie in data['results']:
    movies.append({
        'title': movie['title'],
        'genres': ', '.join([genre['name'] for genre in movie['genre_ids']]),  # Join genres as comma-separated string
        'rating': movie['vote_average'],
        'release_year': movie['release_date'][:4],  # Extract year from release date
        'length': movie.get('runtime', 0)  # Assuming runtime is included, default to 0 if not available
    })

# Create a DataFrame
df_global = pd.DataFrame(movies)

# Save to CSV for future use
RATINGS_FILE = "global_ratings.csv"
df_global.to_csv('RATINGS_FILE.csv', index=False)

# Display the DataFrame
st.write("Global Ratings Data")
st.dataframe(df_global.head())

