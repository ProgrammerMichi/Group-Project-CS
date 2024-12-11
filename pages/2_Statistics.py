import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the ratings data from the CSV file
ratings_df = pd.read_csv("ratings_with_genres_sample.csv")

# Preprocess the data to calculate average ratings per genre
ratings_df['primary_genre'] = ratings_df['genres'].apply(lambda x: x.split(',')[0])

# Bar chart for Average Rating by Genre
genre_avg_ratings = ratings_df.groupby('primary_genre')['rating'].mean().sort_values(ascending=False)
st.title("Average Movie Ratings by Genre")
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x=genre_avg_ratings.index, y=genre_avg_ratings.values, ax=ax)
ax.set_ylabel('Average Rating')
ax.set_xlabel('Genre')
ax.set_title('Average Movie Ratings by Genre')
st.pyplot(fig)

# Histogram of Rating Distribution
st.title("Distribution of Movie Ratings")
fig, ax = plt.subplots(figsize=(10, 6))
sns.histplot(ratings_df['rating'], kde=True, ax=ax, bins=10)
ax.set_xlabel('Rating')
ax.set_ylabel('Frequency')
ax.set_title('Distribution of Movie Ratings')
st.pyplot(fig)

# Pie chart of Genre Distribution
genre_counts = ratings_df['primary_genre'].value_counts()
st.title("Genre Distribution of Movies")
fig, ax = plt.subplots(figsize=(8, 8))
ax.pie(genre_counts, labels=genre_counts.index, autopct='%1.1f%%', startangle=90)
ax.axis('equal')
st.pyplot(fig)

# Scatter plot for Movie ID vs Rating
st.title("Movie Rating vs Movie ID")
fig, ax = plt.subplots(figsize=(10, 6))
sns.scatterplot(x=ratings_df['movieId'], y=ratings_df['rating'], ax=ax)
ax.set_xlabel('Movie ID')
ax.set_ylabel('Rating')
ax.set_title('Movie Rating vs Movie ID')
st.pyplot(fig)


# Display the CSV data as a table
st.title("Movie Ratings with Genres")
st.dataframe(ratings_df)