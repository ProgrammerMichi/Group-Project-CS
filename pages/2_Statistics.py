import streamlit as st
import pandas as pd

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


# Display the CSV data as a table
st.title("Movie Ratings with Genres")
st.dataframe(ratings_df)