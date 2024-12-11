import streamlit as st
import pandas as pd

# Load the ratings data from the CSV file
ratings_df = pd.read_csv("ratings_with_genres_sample.csv")

# Display the CSV data as a table
st.title("Movie Ratings with Genres")
st.dataframe(ratings_df)