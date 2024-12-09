from tmdbv3api import Discover, Person, Genre
from APIConnection import TMDbAPIClient
from app import Instance

from app import selgen
from app import selactor
from app import selkeywords
from app import selmin_rating
from app import selmax_rating
from app import selmin_votes
from app import selmin_length
from app import selmax_length
from app import selrel_after
from app import selrel_before
from app import genre_check
from app import actor_check
from app import keyword_check
from app import rating_check
from app import length_check
from app import date_check





def findmovie():
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

    moviesfound = Instance.discover.movie({
        "sort_by": "vote_average.desc",
        "with_genres": str(Instance.get_genre_id(genre)),
        "with_cast": str(Instance.person.search(actor)),
        "with_keywords": str(keywords),
        "vote_average.gte": str(min_rating),
        "vote_average.lte": str(max_rating),
        "vote_count.gte": str(min_votes),
        "with_runtime.gte": str(min_length),
        "with_runtime.lte": str(max_length),
        "primary_release_date.gte": str(rel_after),
        "primary_release_date.lte": str(rel_before),
        })    
    
    return moviesfound