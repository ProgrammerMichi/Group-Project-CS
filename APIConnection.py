#This is the connection point between code and the TMDB API

from tmdbv3api import TMDb, Movie, Genre


#Temporary placeholder
API_KEY = 20

class TMDbAPIClient:
    def __init__(self, api_key=None):
        self.tmdb = TMDb()

        #The API_Key should be either implemented through an environment variable or streamlit/github secrets
        self.tmdb.api_key = API_KEY
        self.movie_api = Movie()
        self.genre_api = Genre()


    def search_movie_title(self, query):
        #Looks for a movie title based on query
        return self.movie_api.search(query)
    
    
    def get_genres(self, movie_genre ):
        #Looks for genres in API
        genres = self.genre_api.popular()
        return genres
    
    
    def get_movie_by_genres(self, genre_id, page=1):
        #Looks for movies according to genre
        movies = self.movie_api.discover(page=page, with_genres=genre_id)
        return movies
    
    
    def search_movie_actors(self, movie_id):
        #Gets actors of a movie based on movie id
        movie_details = self.movie_api.details(movie_id)
        return movie_details.get("cast",[])
    

    def search_movie_length(self, min_length, max_length):
        #Looks for a movie depending on length
        moviesbeforefilter = self.movie_api.popular()
        filtered_movies = [movie for movie in moviesbeforefilter
                           if min_length <= movie["runtime"] <= max_length]
        return filtered_movies
    
        
    def search_movie_by_keywords(self, keyword):
        #Looks for a movie depending on keywords
        return self.movie_api.search(keyword)
    
    
    def get_movie_details(self, movie_id):
        #Gets information to a film
        return self.movie_api.details(movie_id)
    
    
    def get_recommendations(self, movie_id):
        #Generates a recommendation based on a movie
        return self.movie_api.recommendations(movie_id)
    
    
    def get_popular_movie(self):
        #List of most popular films
        return self.movie_api.popular()