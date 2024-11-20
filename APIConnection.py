#This is the connection to the TMDB API

from tmdbv3api import TMDb, Movie

class TMDbAPIClient:
    def __init__(self, api_key):
        self.tmdb = TMDb()
        self.tmdb.api_key = api_key
        self.movie_api = Movie()

    def search_movie