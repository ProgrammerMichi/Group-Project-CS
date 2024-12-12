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

# Distribution of Movie Ratings
fig1 = px.histogram(df_ratings, x="rating", nbins=10, title="Distribution of Movie Ratings")
fig1.show()

# Average Rating by Genre
# Split genres into multiple rows
df_genres = df_ratings.assign(genres=df_ratings['genres'].str.split(', ')).explode('genres')
avg_rating_by_genre = df_genres.groupby('genres')['rating'].mean().reset_index()
fig2 = px.bar(avg_rating_by_genre, x="genres", y="rating", title="Average Rating by Genre")
fig2.show()


# Number of Movies by Release Year
movies_by_year = df_ratings.groupby('release_year').size().reset_index(name='count')
fig4 = px.bar(movies_by_year, x="release_year", y="count", title="Number of Movies by Release Year")
fig4.show()


# Pie chart with genres
df_genres = df_ratings.assign(genres=df_ratings['genres'].str.split(', ')).explode('genres')
genre_counts = df_genres['genres'].value_counts().reset_index()
genre_counts.columns = ['genres', 'count']
fig5 = px.pie(genre_counts, names='genres', values='count', title='Distribution of Genres')
fig5.show()

# Radar chart for similarities (example using average rating by genre)
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
            range=[0, 10]
        )),
    showlegend=False,
    title='Radar Chart for Average Ratings by Genre'
)
fig6.show()

# Total movie runtime for each genre
genre_runtime = df_genres.groupby('genres')['length'].sum().reset_index()
fig7 = px.bar(genre_runtime, x='genres', y='length', title='Total Movie Runtime for Each Genre')
fig7.show()
