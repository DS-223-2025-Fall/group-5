import streamlit as st

def settings_screen():
    st.title("Settings")
    
    # Input fields for settings
    username = st.text_input("Change Username", value="User123")
    st.write(f"Current Username: {username}")
    
    # Option to change app theme (dark or light)
    theme = st.selectbox("Choose App Theme", ["Light", "Dark"])
    if theme == "Dark":
        st.markdown(
            """
            <style>
            .main {
                background-color: #2b2b2b;
                color: white;
            }
            </style>
            """, unsafe_allow_html=True
        )
    else:
        st.markdown(
            """
            <style>
            .main {
                background-color: white;
                color: black;
            }
            </style>
            """, unsafe_allow_html=True
        )
    
    # Example: Save settings (this is just a placeholder for later functionality)
    if st.button("Save Settings"):
        st.success("Settings saved successfully!")
