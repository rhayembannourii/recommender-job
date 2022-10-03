import streamlit as st
from data_base import login_user  # connect_base,
# import sqlite3
from main import switch_page

# cc,_=connect_base()

st.title('Login Section.')
username = st.text_input("User Name")
password = st.text_input("Password", type="password")
if st.button("Login"):
    result = login_user(username, password)
    if result:
        # st.success("Logged In as {}".format(username))
        # job_recommender()
        switch_page('company')
    else:
        st.warning("Incorrect username/password ")
