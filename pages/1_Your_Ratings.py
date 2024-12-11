import streamlit as st

# Tab Title, Titles and Intro
st.set_page_config(page_title="Ratings", page_icon="📋", layout="wide")
st.title("Your Movie Ratings")
st.write("...")

st.header("Rate our recommendations")
st.write("In order to improve our services for you, please rate your satisfaction with our recommendations.")


st.header("Rate Movies you have previously watched")
st.write("Here you can find all the movies you have already watched")



# stars for ratings
sentiment_mapping = ["one", "two", "three", "four", "five"]
selected = st.feedback("stars")
if selected is not None:
    st.markdown(f"You selected {sentiment_mapping[selected]} star(s).")
