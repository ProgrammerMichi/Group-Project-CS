import streamlit as st
pip install streamlit-extras
from streamlit_extras.switch_page_button import switch_page

def example():
    want_to_contribute = st.button("I want to contribute!")
    if want_to_contribute:
        switch_page("Ratings")

if st.button("Get started"):
    st.switch_page("app.py")
if st.button("Rate our Recommendations"):
    st.switch_page("pages/1_Ratings.py")
if st.button("See your statistics"):
    st.switch_page("pages/2_Statistics.py")

app_path = 'https://groupemichi.streamlit.app'
page_file_path = 'pages/Ratings.py'
page = page_file_path.split('/')[1][0:-3]  # get "1_Ratings.py"
st.write("Rate our Recommendations") 
st.markdown(
    f'''<a href="{app_path}/{page}" target="_self">here</a>''',
    unsafe_allow_html=True
)

url = "https://groupemichi.streamlit.app"
st.write("get started [here](%s)" % url)


