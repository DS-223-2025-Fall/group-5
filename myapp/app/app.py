import streamlit as st
from login import login_screen
from dashboard import dashboard_screen
from upload import upload_screen
from bundles import bundles_screen
from campaign import campaigns_screen
from settings import settings_screen
from db import get_db_connection
import base64

def load_image_base64(path):
    with open(path, "rb") as img:
         return base64.b64encode(img.read()).decode()

logo = load_image_base64("assets/clustr.png")

# ---- Global page config ----
st.set_page_config(
    page_title="Clustr | Smart Bundling Optimizer",
    page_icon="📦",
    layout="wide",
)

# ---- Global CSS & Dark Theme ----
GLOBAL_CSS = """
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>
/* Base app styles */
.stApp {
    background-color: #1d293d;
    color: #ffffff;
    font-family: 'Space Grotesk', sans-serif;
}

/* Sidebar text - make white */
.stSidebar * {
    color: #ffffff !important;
}

</style>
"""

# ---- Login callback ----
def on_login():
    st.session_state.logged_in = True
    st.session_state.current_screen = "Database"
    # Initialize DB connection on login
    db_info = get_db_connection()
    if db_info:
        st.session_state["db_conn"] = db_info["connection"]
        st.session_state["db_engine"] = db_info["engine"]



# ---- Sidebar Navigation ----

def navigation():
    if "current_screen" not in st.session_state:
        st.session_state.current_screen = "Database"

    with st.sidebar:
        st.markdown(
        f"""
        <div style="display: flex; justify-content: center;">
            <img src="data:image/png;base64,{logo}" width="220">
        </div>
        """,
        unsafe_allow_html=True,
    )
        st.markdown("### Navigation")
        choice = st.pills(
            "Go to",
            options=["Database", "Dashboard", "Bundle Suggestions", "Campaigns", "Settings"],
            default=st.session_state.current_screen
        )
        st.session_state.current_screen = choice

        st.markdown("---")
        if st.button("Log out"):
            st.session_state.clear()
            st.rerun()


    # Ensure DB connection
    if "db_conn" not in st.session_state:
        db_info = get_db_connection()
        if db_info:
            st.session_state.db_conn = db_info["connection"]
            st.session_state.db_engine = db_info["engine"]

    # Routing
    screen = st.session_state.current_screen
    if screen == "Database":
        upload_screen()
    elif screen == "Dashboard":
        dashboard_screen()
    elif screen == "Bundle Suggestions":
        bundles_screen()
    elif screen == "Campaigns":
        campaigns_screen()
    elif screen == "Settings":
        settings_screen()
    else:
        upload_screen()

# ---- Card Helper ----
def card(content_func):
    """Wrap Streamlit content inside a card."""
    st.markdown('<div class="card">', unsafe_allow_html=True)
    content_func()
    st.markdown('</div>', unsafe_allow_html=True)

# ---- Main ----
def main():
    # Inject global CSS
    if "css_loaded" not in st.session_state:
        st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
        st.session_state.css_loaded = True

    # Login state
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        login_screen(on_login)
    else:
        navigation()

if __name__ == "__main__":
    main()