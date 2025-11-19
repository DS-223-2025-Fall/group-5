import streamlit as st
import pandas as pd

def upload_screen():
    st.title("Upload Data")
    
    # Allow user to upload a file
    uploaded_file = st.file_uploader("Choose a file", type=["csv", "xlsx", "txt"])
    
    if uploaded_file is not None:
        # Show file name
        st.write("File uploaded:", uploaded_file.name)
        
        # Process the file based on the type
        if uploaded_file.name.endswith('.csv'):
            data = pd.read_csv(uploaded_file)
            st.write(data)  # Display the dataframe
        elif uploaded_file.name.endswith('.xlsx'):
            data = pd.read_excel(uploaded_file)
            st.write(data)  # Display the dataframe
        elif uploaded_file.name.endswith('.txt'):
            text = uploaded_file.read().decode("utf-8")
            st.text(text)  # Display text content
