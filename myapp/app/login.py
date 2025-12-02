import streamlit as st
import base64

# ============================================================
#        REMOVE ALL STREAMLIT DEFAULT ELEMENTS
# ============================================================
st.markdown("""
    <style>
    /* Remove ALL Streamlit branding and padding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    [data-testid="stToolbar"] {
        display: none !important;
    }
    
    [data-testid="stDecoration"] {
        display: none !important;
    }
    
    [data-testid="stStatusWidget"] {
        display: none !important;
    }
    
    /* Remove top header/navbar */
    [data-testid="stHeader"] {
        display: none !important;
        height: 0 !important;
    }
    
    /* Remove all padding and margins */
    .main .block-container {
        padding: 0 !important;
        padding-bottom: 2rem !important;
        max-width: 100% !important;
    }
    
    .stApp {
        margin: 0 !important;
        padding: 0 !important;
    }
    
    /* Make full screen */
    html, body, [data-testid="stAppViewContainer"], .main {
        height: 100% !important;
        overflow: hidden !important;
    }
    </style>
""", unsafe_allow_html=True)


# ============================================================
#                      LOGIN SCREEN UI
# ============================================================
def login_screen(on_login):
    # Load background image
    def load_image_base64(path):
        with open(path, "rb") as img:
            return base64.b64encode(img.read()).decode()

    try:
        bg_image = load_image_base64("assets/landing.png")
    except FileNotFoundError as e:
        st.error(f"Image not found: {e}")
        return

    st.markdown(f"""
        <style>
        /* Full screen background */
        .stApp {{
            background-image: url("data:image/png;base64,{bg_image}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
            height: 100vh;
            overflow: hidden;
        }}

        /* Login form container - fixed at bottom */
        .login-form-wrapper {{
            position: fixed;
            bottom: 2rem;
            left: 50%;
            transform: translateX(-50%);
            width: 90%;
            max-width: 450px;
            z-index: 1000;
        }}

        /* Style form inputs with glass effect */
        .stTextInput > div > div > input {{
            background: rgba(15, 23, 42, 0.4) !important;
            backdrop-filter: blur(12px) !important;
            -webkit-backdrop-filter: blur(12px) !important;
            color: #ffffff !important;
            border: 1px solid rgba(139, 92, 246, 0.3) !important;
            border-radius: 12px !important;
            padding: 0.875rem 1rem !important;
            font-size: 15px !important;
        }}

        .stTextInput > div > div > input:focus {{
            border-color: #8b5cf6 !important;
            box-shadow: 0 0 0 2px rgba(139, 92, 246, 0.2) !important;
            background: rgba(15, 23, 42, 0.5) !important;
        }}

        .stTextInput > div > div > input::placeholder {{
            color: #94a3b8 !important;
        }}

        /* Labels */
        .stTextInput > label {{
            color: #e2e8f0 !important;
            font-weight: 500 !important;
            font-size: 14px !important;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5) !important;
        }}

        /* Style submit button */
        .stButton > button {{
            width: 100%;
            background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
            color: white !important;
            border: none !important;
            padding: 0.875rem 1.5rem !important;
            border-radius: 12px !important;
            font-weight: 600 !important;
            font-size: 16px !important;
            transition: all 0.3s ease !important;
            margin-top: 1rem !important;
            box-shadow: 0 4px 15px rgba(139, 92, 246, 0.4) !important;
        }}

        .stButton > button:hover {{
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 25px rgba(139, 92, 246, 0.5) !important;
        }}

        /* Error messages */
        .stAlert {{
            background-color: rgba(239, 68, 68, 0.15) !important;
            backdrop-filter: blur(12px) !important;
            border: 1px solid rgba(239, 68, 68, 0.3) !important;
            border-radius: 10px !important;
            color: #fecaca !important;
        }}

        /* Hide form border */
        [data-testid="stForm"] {{
            border: none !important;
            background: transparent !important;
        }}
        </style>
    """, unsafe_allow_html=True)

    # Create a large spacer to push form down
    st.markdown('<div style="height: 35vh; width: 100%;"></div>', unsafe_allow_html=True)

    # Login form at bottom
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.form("login_form"):
            username = st.text_input("Email or username", placeholder="you@example.com")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            submitted = st.form_submit_button("Sign in")

        if submitted:
            if username.strip() and password.strip():
                on_login()
                st.rerun()
            else:
                st.error("Please fill in all fields.")