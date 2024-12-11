import streamlit as st
import pandas as pd
import plotly_express as px


# Load the ratings data from the CSV file
ratings_df = pd.read_csv("ratings_with_genres_sample.csv")

# Preprocess the data to calculate average ratings per genre
ratings_df['primary_genre'] = ratings_df['genres'].apply(lambda x: x.split(',')[0])

# Interactive Bar Chart using Plotly (optional)
genre_avg_ratings = ratings_df.groupby('primary_genre')['rating'].mean().reset_index()
fig = px.bar(genre_avg_ratings, x='primary_genre', y='rating', 
             title="Average Rating by Genre", 
             labels={'primary_genre': 'Genre', 'rating': 'Average Rating'})
st.plotly_chart(fig)


# Display the CSV data as a table
st.title("Movie Ratings with Genres")
st.dataframe(ratings_df)