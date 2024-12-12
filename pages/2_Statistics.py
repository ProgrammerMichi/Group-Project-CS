import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os


# Tab Title, Title and Intro
st.set_page_config(page_title="Statistics", page_icon="📊", layout="wide")
st.title("Your Statistics")
st.write("Here you can find diverse charts visualising all of your rated movies.")


# Load the dataset
df_ratings = pd.read_csv("ratings_with_genres_and_details_sample.csv")

global_ratings_path = "global_ratings.csv"


col1, col2 = st.columns([1, 1])

with col1:
    # Bar chart showing the average rating by genre
    df_genres = df_ratings.assign(genres=df_ratings['genres'].str.split(', ')).explode('genres')
    avg_rating_by_genre = df_genres.groupby('genres')['rating'].mean().reset_index()
    fig1 = px.bar(avg_rating_by_genre, x="genres", y="rating", title="Average Rating by Genre")
    fig1.update_layout(
        xaxis_title="Genres",
        yaxis_title="Average Rating")
    st.plotly_chart(fig1)
    # Determine and display the best-rated genre
    best_rated_genre = avg_rating_by_genre.loc[avg_rating_by_genre['rating'].idxmax()]
    st.write(f"Your best-rated genre is '{best_rated_genre['genres']}' with an average rating of {best_rated_genre['rating']}.")

with col2:
    # Radar chart for average rating by genre
    genre_ratings = df_genres.groupby('genres')['rating'].mean().reset_index()
    fig2 = go.Figure()
    fig2.add_trace(go.Scatterpolar(
        r=genre_ratings['rating'],
        theta=genre_ratings['genres'],
        fill='toself'
    ))
    fig2.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 10],
                tickfont=dict(color='black')
            )),
        showlegend=False,
        title='Average Rating by Genre'
    )
    st.plotly_chart(fig2)


col3, col4 = st.columns([1, 1])

with col3:
    # Bar Chart showing the total movie runtime for each genre
    genre_runtime = df_genres.groupby('genres')['length'].sum().reset_index()
    fig3 = px.bar(genre_runtime, x='genres', y='length', title='Total Movie Runtime for Each Genre')
    fig3.update_layout(
        xaxis_title="Genres",
        yaxis_title="Total Runtime (minutes)")
    st.plotly_chart(fig3)
    # Determine and display the most watched genre
    most_watched_genre_runtime = df_genres.groupby('genres')['length'].sum().idxmax()
    st.write(f"Your most watched genre by total runtime is '{most_watched_genre_runtime}'.")

with col4:
    # Pie chart showing the portion of genres for all rated movies
    df_genres = df_ratings.assign(genres=df_ratings['genres'].str.split(', ')).explode('genres')
    genre_counts = df_genres['genres'].value_counts().reset_index()
    genre_counts.columns = ['genres', 'count']
    fig4 = px.pie(genre_counts, names='genres', values='count', title='Distribution of Genres')
    st.plotly_chart(fig4)
    # Determine and display the genre with the most movies
    most_movies_genre = genre_counts.iloc[0]
    st.write(f"The genre that holds the most movies is '{most_movies_genre['genres']}' with {most_movies_genre['count']} movies.")



# Bar chart showing the number of movies rated by release year
movies_by_year = df_ratings.groupby('release_year').size().reset_index(name='count')
fig5 = px.bar(movies_by_year, x="release_year", y="count", title="Number of Rated Movies by Release Year")
fig5.update_layout(
    width=900,
    xaxis_title="Release Year",
    yaxis_title="Number of Movies")
st.plotly_chart(fig5)
# Determine and display the year with the most movies
most_watched_year = df_ratings['release_year'].value_counts().idxmax()
st.write(f"You have mostly watched movies released in {most_watched_year}.")


# 5. Top-Rated Movies by the User
top_rated = df_ratings.sort_values('rating', ascending=False).head(10)
fig6 = px.bar(top_rated, x='rating', y='title', orientation='h',
             title="Top-Rated Movies",
             labels={'title': 'Movie', 'rating': 'Rating'})
st.plotly_chart(fig6)


if os.path.exists(global_ratings_path):
    df_global = pd.read_csv(global_ratings_path)
    st.write("Global Ratings Data")
    st.dataframe(df_global.head())
    
    # Check if the necessary columns are present
    if 'genres' in df_global.columns and 'rating' in df_global.columns:
        # Generate and display the comparison chart
        def generate_comparison_chart(df_user, df_global):
            user_avg_ratings = df_user.groupby('genres')['rating'].mean().reset_index()
            user_avg_ratings.columns = ['genres', 'user_avg_rating']

            global_avg_ratings = df_global.groupby('genres')['rating'].mean().reset_index()
            global_avg_ratings.columns = ['genres', 'global_avg_rating']

            comparison_df = pd.merge(user_avg_ratings, global_avg_ratings, on='genres')

            fig = px.bar(comparison_df, x='genres', y=['user_avg_rating', 'global_avg_rating'],
                         title='Comparison of User Rating Patterns Against Global Averages',
                         labels={'value': 'Average Rating', 'variable': 'Rating Type'},
                         barmode='group')

            fig.update_layout(
                xaxis_title="Genres",
                yaxis_title="Average Rating",
                xaxis=dict(title_font=dict(size=18)),
                yaxis=dict(title_font=dict(size=18)),
                title=dict(font=dict(size=24))
            )

            return fig

        # Generate and display the comparison chart
        fig = generate_comparison_chart(df_ratings, df_global)
        st.plotly_chart(fig)
    else:
        st.error("The 'global_ratings.csv' file does not contain the necessary columns 'genres' and 'rating'.")
else:
    st.error("The global ratings file 'global_ratings.csv' was not found. Please ensure it exists in the correct directory.")
