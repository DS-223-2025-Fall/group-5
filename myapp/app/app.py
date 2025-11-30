import streamlit as st

from login import login_screen
from dashboard import dashboard_screen
from upload import upload_screen
from bundles import bundles_screen
from performance import performance_screen
from settings import settings_screen


# ---- Global page config ----
st.set_page_config(
    page_title="Clustr | Smart Bundling Optimizer",
    page_icon="📦",
    layout="wide",
)

GLOBAL_CSS = """
<style>
.stApp {
    background: radial-gradient(circle at top left, #e0f2fe 0, #f8fafc 40%, #eef2ff 100%);
    font-family: system-ui, -apple-system, BlinkMacSystemFont, "SF Pro Text",
                 "Segoe UI", sans-serif;
}

/* card look */
.card {
    background-color: #ffffff;
    border-radius: 18px;
    padding: 1.25rem 1.5rem;
    border: 1px solid #e2e8f0;
    box-shadow: 0 18px 45px rgba(15, 23, 42, 0.06);
}

/* simple top nav bar */
.top-nav {
    padding: 0.6rem 1.2rem;
    margin-bottom: 1.0rem;
}
.top-nav-inner {
    display:flex;
    align-items:center;
    justify-content:space-between;
    gap:1.5rem;
}
.top-nav-left {
    display:flex;
    align-items:center;
    gap:0.75rem;
}
.top-nav-logo {
    width:28px;
    height:28px;
    border-radius:8px;
    background:#2563eb1a;
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:18px;
}
.top-nav-title {
    font-weight:600;
    color:#0f172a;
    font-size:15px;
}
.top-nav-subtitle {
    font-size:11px;
    color:#64748b;
}
.top-nav-user {
    font-size:12px;
    color:#64748b;
}

/* login centering */
.login-wrapper {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}
.login-card {
    max-width: 440px;
    width: 100%;
}
</style>
"""


def on_login():
    """Called by login_screen when user logs in successfully."""
    st.session_state.logged_in = True
    # First thing after login: go to Upload page so they connect data
    st.session_state.current_screen = "Upload"


def render_top_nav():
    st.markdown('<div class="card top-nav"><div class="top-nav-inner">', unsafe_allow_html=True)

    left_html = """
        <div class="top-nav-left">
          <div class="top-nav-logo">Clustr</div>
          <div>
            <div class="top-nav-subtitle">Smart Bundling Optimizer</div>
          </div>
        </div>
    """
    st.markdown(left_html, unsafe_allow_html=True)

    # right part – username info
    st.markdown(
        '<div class="top-nav-user">Demo User • user@example.com</div></div></div>',
        unsafe_allow_html=True,
    )


def navigation():
    """Main routing logic after login."""
    if "current_screen" not in st.session_state:
        st.session_state.current_screen = "Upload"

    # Sidebar navigation
    with st.sidebar:
        st.markdown("### Navigation")
        choice = st.radio(
            "Go to",
            ["Upload", "Dashboard", "Bundle Suggestions", "Performance", "Settings"],
            index=["Upload", "Dashboard", "Bundle Suggestions", "Performance", "Settings"]
            .index(st.session_state.current_screen),
        )
        st.session_state.current_screen = choice

        st.markdown("---")
        if st.button("Log out"):
            st.session_state.clear()
            st.rerun()

    # Top nav bar (visual only)
    render_top_nav()

    # Route to selected screen
    screen = st.session_state.current_screen

    if screen == "Upload":
        upload_screen()
    elif screen == "Dashboard":
        dashboard_screen()
    elif screen == "Bundle Suggestions":
        bundles_screen()
    elif screen == "Performance":
        performance_screen()
    elif screen == "Settings":
        settings_screen()
    else:
        upload_screen()


def main():
    # Inject global CSS once
    if "css_loaded" not in st.session_state:
        st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
        st.session_state.css_loaded = True

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        # Show login screen and pass callback
        login_screen(on_login)
    else:
        navigation()


if __name__ == "__main__":
    main()
