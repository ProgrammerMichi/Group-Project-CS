import streamlit as st
import pandas as pd
import plotly.express as px


# Tab Title, Title and Intro
st.set_page_config(page_title="Statistics", page_icon="📊", layout="wide")
st.title("Your Statistics")
st.write("""Here you can find diverse charts ...""")


# Load the ratings data from the CSV file
ratings_df = pd.read_csv("ratings_with_genres_sample.csv")

# Preprocess the data to calculate average ratings per genre
ratings_df['primary_genre'] = ratings_df['genres'].apply(lambda x: x.split(',')[0])

# Interactive Bar Chart using Plotly
genre_avg_ratings = ratings_df.groupby('primary_genre')['rating'].mean().reset_index()
fig = px.bar(genre_avg_ratings, x='primary_genre', y='rating', 
             title="Average Rating by Genre", 
             labels={'primary_genre': 'Genre', 'rating': 'Average Rating'})
fig.update_layout(width=900)
st.plotly_chart(fig)


# pie chart with genres
# radar chart for similarities
# list of top and worst rated movies
# average rating by release date
# total time for each genre


# Display the CSV data as a table
st.title("Movie Ratings with Genres")
st.dataframe(ratings_df)
