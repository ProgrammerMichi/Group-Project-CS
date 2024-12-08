import streamlit as st

if st.button("Home"):
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
