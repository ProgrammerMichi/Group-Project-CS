import requests
import pandas as pd

# Define your TMDB API key and endpoint
api_key = 'your_tmdb_api_key'
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
df_global.to_csv('global_ratings.csv', index=False)

# Display the DataFrame
print(df_global.head())

