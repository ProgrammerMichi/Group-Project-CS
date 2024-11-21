import streamlit as st
import os

#Check whether Code runs locally or on Streamlit, to decide whether .env file should be loaded
if os.getenv("STREAMLIT_SERVER") is None:
    from dotenv import load_dotenv
    load_dotenv()




st.write ("hooray we connected anana sikim")