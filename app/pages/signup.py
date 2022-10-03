import streamlit as st
from data_base import create_usertable, add_userdata  # connect_base,
from main import switch_page

# c,conn=connect_base()

st.subheader("Create New Account")
new_username = st.text_input("User Name")
new_password = st.text_input("Password", type="password")
if st.button("Signup"):
    create_usertable()
    add_userdata(new_username, new_password)
    st.success("You have successfully created a valid aacount")
    st.info("Go to Login menu to login")
    switch_page('login')
