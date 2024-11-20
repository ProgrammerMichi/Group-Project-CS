#This is the connection to the TMDB API

from tmdbv3api import TMDb, Movie

class TMDbAPIClient:
    def __init__(self, api_key):
        self.tmdb = TMDb()
        self.tmdb.api_key = api_key
        self.movie_api = Movie()

    def search_movie(self, query):
        #Looks for a movie depending on title
        return self.movie_api.search(query)
    
    def get_movie_details(self, movie_id):
        #Gets the details to a film
        return self.movie_api.details(movie_id)
    
    def get_recommendations(self, movie_id):
        #Generates a recommendation based on a movie
        return self.movie_api.recommendations(movie_id)
    
    def get_popular_movie(self):
        #List of most popular films
        return self.movie_api.popular()
    
