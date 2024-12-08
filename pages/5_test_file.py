import streamlit as st

app_path = 'https://groupemichi.streamlit.app'
page_file_path = 'pages/Ratings.py'
page = page_file_path.split('/')[1][0:-3]  # get "1_Ratings.py"
st.write("Rate our Recommendations") 
st.markdown(
    f'''<a href="{app_path}/{page}" target="_self">here</a>''',
    unsafe_allow_html=True
)
