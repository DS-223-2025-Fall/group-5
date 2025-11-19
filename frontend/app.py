import streamlit as st
from login import login_screen
from dashboard import dashboard_screen
from upload import upload_screen
from bundles import bundles_screen
from performance import performance_screen
from settings import settings_screen

# Define the on_login function
def on_login():
    # Set the logged_in flag to True when the user logs in
    st.session_state.logged_in = True

# Function to display different screens after login
def navigation():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    
    if st.session_state.logged_in:
        # Display a selectbox (or sidebar) for navigation
        screen = st.selectbox("Choose Screen", ["Dashboard", "Upload", "Bundles", "Performance", "Settings"])
        
        # Display the corresponding screen based on the user's selection
        if screen == "Dashboard":
            dashboard_screen()
        elif screen == "Upload":
            upload_screen()
        elif screen == "Bundles":
            bundles_screen()
        elif screen == "Performance":
            performance_screen()
        elif screen == "Settings":
            settings_screen()
    else:
        # Show the login screen if the user is not logged in
        login_screen(on_login)  # Pass the on_login function

# Main function
def main():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    
    # Call the navigation function to display the appropriate screen
    navigation()

if __name__ == "__main__":
    main()
