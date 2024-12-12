import requests
import pandas as pd

# Define your TMDB API key
api_key = 'your_tmdb_api_key'

def fetch_movies(endpoint, params, max_pages=5):
    movies = []
    for page in range(1, max_pages + 1):
        params['page'] = page
        response = requests.get(endpoint, params=params)
        data = response.json()
        for movie in data['results']:
            movies.append({
                'title': movie['title'],
                'genres': ', '.join([genre['name'] for genre in movie['genre_ids']]),
                'rating': movie['vote_average'],
                'release_year': movie['release_date'][:4],
                'length': movie.get('runtime', 0)
            })
    return movies

def get_all_movies():
    popular_endpoint = 'https://api.themoviedb.org/3/movie/popular'
    popular_params = {'api_key': api_key, 'language': 'en-US'}
    popular_movies = fetch_movies(popular_endpoint, popular_params)

    top_rated_endpoint = 'https://api.themoviedb.org/3/movie/top_rated'
    top_rated_params = {'api_key': api_key, 'language': 'en-US'}
    top_rated_movies = fetch_movies(top_rated_endpoint, top_rated_params)

    return popular_movies + top_rated_movies

def save_global_ratings_to_csv():
    all_movies = get_all_movies()
    df_global = pd.DataFrame(all_movies)
    df_global.to_csv('global_ratings.csv', index=False)