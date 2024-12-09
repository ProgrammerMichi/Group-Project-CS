from tmdbv3api import Discover
from APIConnection import TMDbAPIClient
from app import Instance



selgen = None
selactor = None
selkeywords = None
selmin_rating = None
selmax_rating = None
selmin_votes = None
selmin_length = None
selmax_length = None
selrel_after = None
selrel_before = None
genre_check = None
actor_check = None
keyword_check = None
rating_check = None
min_length = None
length_check = None
date_check = None


def findmovie(self, x):
    if genre_check:
        genre = selgen
    
    if actor_check:
        actor = selactor

    if keyword_check:
        keywords = selkeywords

    if rating_check:
        min_rating = selmin_rating
        max_rating = selmax_rating
        min_votes = selmin_votes

    if length_check:
        min_length = selmin_length
        max_length = selmax_length

    if date_check:
        rel_after = selrel_after
        rel_before = selrel_before

    moviesfound = Instance.discover.movie(
        sort_by: "vote_average.desc",
        with_genres: Instance.get_genre_id(genre)
        with_cast: Instance.person.search(actor)
        with_keywords: keywords
        vote_average.gte: min_rating
        vote_average.gte: max_rating
        vote_count.gte: min_votes
        with_runtime.gte: min_length
        with_runtime.lte: max_length
        primary_release_date.gte: rel_after
        primary_release_date.lte: rel_before
    )
    returnmovies = []
    if moviesfound:
        for movie in moviesfound:
            returnmovies.append({movie["title"]})
        
    return returnmovies