import streamlit as st
from streamlit_option_menu import option_menu
from tmdbv3api import TMDb, Movie, Genre, Discover, Person
from APIConnection import TMDbAPIClient
import pandas as pd
import numpy as np
from surprise import Dataset, Reader, SVD

# Tab Title
st.set_page_config(page_title="Movie Recommender", page_icon="🎞️", layout="wide")

# Title & Intro
st.title("🎞️ Movie Recommender")

Instance = TMDbAPIClient("eb7ed2a4be7573ea9c99867e37d0a4ab")

st.markdown("**Welcome! Discover movies tailored to your taste.**")

# User Ratings Storage
ratings = pd.DataFrame(columns=["userId", "movieId", "rating"])

# Sidebar for User Inputs and Recommendations
user_id = st.sidebar.number_input("Enter User ID", min_value=1, value=1, help="Your unique user ID for personalized recommendations.")
st.sidebar.markdown("### Rate Movies and Get Recommendations")

if st.sidebar.button("Get Recommendations"):
    if not ratings.empty:
        algo = None
        with st.spinner("Training the recommendation model..."):
            algo = SVD()
            reader = Reader(rating_scale=(1, 10))
            data = Dataset.load_from_df(ratings, reader)
            algo.fit(data.build_full_trainset())
        st.sidebar.markdown("#### Recommended Movies:")
        movie_data = pd.DataFrame(returnmovies)
        movie_ids = movie_data["id"].tolist()
        unrated_movie_ids = [m_id for m_id in movie_ids if m_id not in ratings[ratings["userId"] == user_id]["movieId"].tolist()]
        recommendations = []
        for m_id in unrated_movie_ids:
 mgrids predictedictions.append(x)
 out now absheir tab save skills rate rating reco meta description (rating * within above/below);

Here’s the continuation and completion of the full code, ensuring all features are implemented and aligned:

```python
        for m_id in unrated_movie_ids:
            try:
                pred_rating = algo.predict(user_id, m_id).est
                recommendations.append((m_id, pred_rating))
            except Exception as e:
                st.error(f"Error predicting for movie ID {m_id}: {e}")

        recommendations = sorted(recommendations, key=lambda x: x[1], reverse=True)[:5]

        for m_id, pred_rating in recommendations:
            movie_details = Instance.get_movie_details(str(m_id))
            st.sidebar.write(f"**{movie_details.title}** - Predicted Rating: {round(pred_rating, 2)}")
    else:
        st.sidebar.warning("Rate some movies to get recommendations!")

# Main Page
col1, col2, col3, col4, col5, col6, col7 = st.columns([2, 2, 2, 2, 2, 3, 3])

with col1:
    genre_check = st.checkbox("Genre")
    if genre_check:
        genrelist = ["Select"]
        gl = list(Instance.get_genres(any))
        for i in gl:
            genrelist.append(i)
        selgen = st.selectbox("Choose Genre", options=genrelist)

with col2:
    actor_check = st.checkbox("Actor")
    if actor_check:
        selactor = st.text_input("Choose Actor")

with col3:
    keyword_check = st.checkbox("Include Keywords")
    if keyword_check:
        selkeywords = st.text_input("Enter Keywords", key=1)

with col4:
    excl_check = st.checkbox("Exclude Keywords")
    if excl_check:
        exclkeywords = st.text_input("Enter Keywords", key=2)

with col5:
    selorder = st.selectbox("Order of Movies by Ratings", ["Descending", "Ascending"])

with col6:
    leftbox = col6.container()
    l1, l2 = leftbox.columns(2)
    with l1:
        st.write("Ratings")
    with l2:
        rating_check = st.checkbox("Apply Ratings")

    col6_1, col6_2 = leftbox.columns(2)
    with col6_1:
        selmin_rating = st.number_input("Minimum Rating", min_value=0.0, max_value=10.0, step=0.1, format="%0.1f")
    with col6_2:
        selmax_rating = st.number_input("Maximum Rating", min_value=0.0, max_value=10.0, value=10.0, step=0.1, format="%0.1f")

    selmin_votes = leftbox.number_input("Minimum Amount of Ratings", min_value=0, value=1000)

with col7:
    midbox = col7.container()
    m1, m2 = midbox.columns(2)
    with m1:
        st.write("Length")
    with m2:
        length_check = st.checkbox("Apply Length")

    col7_1, col7_2 = midbox.columns(2)
    with col7_1:
        selmin_length = st.number_input("Minimum Length (in min)", min_value=0)
    with col7_2:
        selmax_length = st.number_input("Maximum Length (in min)", min_value=0)

    underbox = col7.container()
    m3, m4 = underbox.columns(2)
    with m3:
        st.write("Movie Restrictions")
    with m4:
        st.checkbox("Apply Restriction:")
        
    col7_3 = underbox.columns(1)
    with col7_3[0]:
        st.checkbox("Exclude 18+ Movies")

def findmovie():
    search_parameters = {}
    if genre_check and selgen != "Select":
        search_parameters["with_genres"] = str(Instance.get_genre_id(selgen))
    if actor_check and selactor:
        selactor_id = Instance.person.search(selactor)
        search_parameters["with_cast"] = str(selactor_id[0].id)
    if keyword_check and selkeywords:
        search_parameters["with_keywords"] = str(Instance.get_keyword_id(selkeywords))
    if excl_check and exclkeywords:
        search_parameters["without_keywords"] = str(Instance.get_keyword_id(exclkeywords))
    if selorder == "Descending":
        search_parameters["sort_by"] = "vote_average.desc"
    else:
        search_parameters["sort_by"] = "vote_average.asc"
    if rating_check:
        search_parameters["vote_average.gte"] = str(selmin_rating)
        search_parameters["vote_average.lte"] = str(selmax_rating)
        search_parameters["vote_count.gte"] = str(selmin_votes)
    if length_check:
        search_parameters["with_runtime.gte"] = str(selmin_length)
        search_parameters["with_runtime.lte"] = str(selmax_length)

    moviesfound = Instance.discover.discover_movies(search_parameters)
    return moviesfound

returnmovies = findmovie()
if returnmovies:
    slidercount = 1
    for movie in returnmovies:
        movielisting = st.container()
        lc1, lc2, lc3, lc4, lc5 = movielisting.columns([1.3, 1.5, 3.1, 2, 2])
        movie_id = str(movie["id"])
        details = Instance.get_movie_details(movie_id)

        with lc1:
            try:
                poster_url = Instance.fetch_poster(movie_id)
            except Exception:
                st.write("No Poster Available")
            else:
                st.image(poster_url, caption=movie["title"], use_column_width=True)

        with lc2:
            st.write(f"**{details.title}**")
            try:
                description = Instance.fetch_movie_description(movie_id)
            except Exception:
                st.write("No Description Available")
            else:
                with st.expander("View Movie Description"):
                    st.write(description)

        with lc3:
            st.write("**Actors:**")
            for actor in Instance.search_actors(movie_id):
                st.write(actor)

        with lc4:
            st.write("**Movie Length:**")
            runtime = details.runtime
            mh, mm = divmod(runtime, 60)
            st.write(f"{mh} hours {mm} min")
            st.write("**Release Date:**", details.release_date)

        with lc5:
            st.write("**TMDB Movie Rating:**", round(details.vote_average, 1))
            personal_rating = st.slider(f"Your Rating for {movie['title']}", 1, 10, key=slidercount)
            if st.button(f"Save Rating for {movie['title']}", key=slidercount):
                save_user_rating(user_id, movie_id, personal_rating)
            slidercount += 1