#This is the connection to the TMDB API

from tmdbv3api import TMDb, Movie, Genre
#Initializing API Key


tmdb.api_key = "eb7ed2a4be7573ea9c99867e37d0a4ab"

class TMDbAPIClient:
    def __init__(self, api_key=None):
        self.tmdb = TMDb()
        self.tmdb.api_key = eb7ed2a4be7573ea9c99867e37d0a4ab
        self.movie_api = Movie()
        self.genre_api = Genre()


    def search_movie_title(self, query):
        #Looks for a movie title based on query
        return self.movie_api.search(query)
    
    
    def get_genres(self, movie_genre ):
        #Looks for genres in API
        genres = self.genre_api.popular()
        return genres
    
    
    def get_movie_by_genres(self, genre_id, page=1)
        #Looks for movies according to genre
        movies = self.movie_api.discover(page=page, with_genres=genre_id)
        return movies
    
    
    def search_movie_actors(self, movie_actor):
        #Gets actors of a movie based on movie id
        movie_details = self.movie_api.details(movie_id)
        return movie_details.get("cast",[])
    

    def search_movie_length(self, movie_length):
        #Looks for a movie depending on length
        return
    
        
    def search_move_keywords(self, keywords):
        #Looks for a movie depending on keywords
        return 
    
    
    def get_movie_details(self, movie_id):
        #Gets the details to a film
        return self.movie_api.details(movie_id)
    
    
    def get_recommendations(self, movie_id):
        #Generates a recommendation based on a movie
        return self.movie_api.recommendations(movie_id)
    
    
    def get_popular_movie(self):
        #List of most popular films
        return self.movie_api.popular()