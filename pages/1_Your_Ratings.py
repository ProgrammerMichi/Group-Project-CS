import streamlit as st

# Tab Title
st.set_page_config(page_title="Ratiings", page_icon="📋", layout="wide")


# Title & Intro
st.title("How do you rate our recommendations?")
st.write("""
    In order to improve our services for you, please rate your satisfaction with our recommendations.
    """)


# stars for ratings
sentiment_mapping = ["one", "two", "three", "four", "five"]
selected = st.feedback("stars")
if selected is not None:
    st.markdown(f"You selected {sentiment_mapping[selected]} star(s).")
