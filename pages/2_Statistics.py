import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# Tab Title, Title and Intro
st.set_page_config(page_title="Statistics", page_icon="📊", layout="wide")
st.title("Your Statistics")
st.write("""Here you can find diverse charts ...""")


# Load the dataset
df_ratings = pd.read_csv("ratings_with_genres_and_details_sample.csv")


col1, col2 = st.columns([1, 1])

with col1:
    # Bar chart showing the average rating by genre
    df_genres = df_ratings.assign(genres=df_ratings['genres'].str.split(', ')).explode('genres')
    avg_rating_by_genre = df_genres.groupby('genres')['rating'].mean().reset_index()
    fig2 = px.bar(avg_rating_by_genre, x="genres", y="rating", title="Average Rating by Genre")
    fig2.update_layout(
        xaxis_title="Genres",
        yaxis_title="Average Rating")
    st.plotly_chart(fig2)
    # Determine and display the best-rated genre
    best_rated_genre = avg_rating_by_genre.loc[avg_rating_by_genre['rating'].idxmax()]
    st.write(f"Your best-rated genre is '{best_rated_genre['genres']}' with an average rating of {best_rated_genre['rating']}.")

with col2:
    # Radar chart for average ratings by genre
    genre_ratings = df_genres.groupby('genres')['rating'].mean().reset_index()
    fig6 = go.Figure()
    fig6.add_trace(go.Scatterpolar(
        r=genre_ratings['rating'],
        theta=genre_ratings['genres'],
        fill='toself'
    ))
    fig6.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 10],
                tickfont=dict(color='black')
            )),
        showlegend=False,
        title='Average Rating by Genre'
    )
    st.plotly_chart(fig6)

col3, col4 = st.columns([1, 1])

with col3:
    # Bar Chart showing the total movie runtime for each genre
    genre_runtime = df_genres.groupby('genres')['length'].sum().reset_index()
    fig7 = px.bar(genre_runtime, x='genres', y='length', title='Total Movie Runtime for Each Genre')
    fig7.update_layout(width=900,
        xaxis_title="Genres",
        yaxis_title="Total Runtime (minutes)")
    st.plotly_chart(fig7)
    # Determine and display the most watched genre
    most_watched_genre_runtime = df_genres.groupby('genres')['length'].sum().idxmax()
    st.write(f"Your most watched genre by total runtime is '{most_watched_genre_runtime}'.")

with col4:
    # Pie chart showing the portion of genres for all rated movies
    df_genres = df_ratings.assign(genres=df_ratings['genres'].str.split(', ')).explode('genres')
    genre_counts = df_genres['genres'].value_counts().reset_index()
    genre_counts.columns = ['genres', 'count']
    fig5 = px.pie(genre_counts, names='genres', values='count', title='Distribution of Genres')
    fig5.update_layout(width=900)
    st.plotly_chart(fig5)


# Bar chart showing the number of movies rated by release year
movies_by_year = df_ratings.groupby('release_year').size().reset_index(name='count')
fig4 = px.bar(movies_by_year, x="release_year", y="count", title="Number of Movies Rated by Release Year")
fig4.update_layout(
    width=900,
    xaxis_title="Release Year",
    yaxis_title="Number of Movies")
st.plotly_chart(fig4)
# Determine and display the year with the most movies
most_watched_year = df_ratings['release_year'].value_counts().idxmax()
st.write(f"You have mostly watched movies released in {most_watched_year}.")