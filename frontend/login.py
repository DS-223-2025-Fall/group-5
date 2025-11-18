import streamlit as st

def login_screen(on_login):
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if username == "demo" and password == "password":  # Demo login
            on_login()
        else:
            st.error("Invalid credentials")
