import streamlit as st

# ============================================================
#        GLOBAL PAGE FIX — Removes ALL top space, headers,
#        body margin, padding, glow boxes, and empty blocks
# ============================================================
st.markdown("""
    <style>

    /* Remove HTML + BODY margin */
    html, body, .stApp {
        margin: 0 !important;
        padding: 0 !important;
        height: 100% !important;
    }


    /* Remove Streamlit toolbar spacing */
    [data-testid="stToolbar"] {
        display: none !important;
        height: 0 !important;
        padding: 0 !important;
        margin: 0 !important;
    }

    /* Remove block container padding */
    .block-container {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }

    /* Remove internal padding from containers */
    .stElementContainer, .stVerticalBlock, .stMarkdown {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }

    /* Remove glow / shadow background */
    .css-1dp5vir, .css-1kyxreq {
        background: transparent !important;
        box-shadow: none !important;
    }

    </style>
""", unsafe_allow_html=True)



# ============================================================
#                      LOGIN SCREEN UI
# ============================================================
def login_screen(on_login):

    st.markdown("""
        <style>


            .login-title {
                font-size: 42px;
                font-weight: 800;
                text-align: center;
                color: #1e293b;
                margin-top: 10px;
            }

            .login-sub {
                font-size: 20px;
                text-align: center;
                color: #475569;
                margin-bottom: 25px;
            }

        </style>
    """, unsafe_allow_html=True)



    # ---------------- LOGO ----------------
    
# Center ALL images globally

    import base64

    def load_image_base64(path):
        with open(path, "rb") as img:
            return base64.b64encode(img.read()).decode()

    logo = load_image_base64("assets/clustr.png")

    st.markdown(
        f"""
        <div style="display: flex; justify-content: center;">
            <img src="data:image/png;base64,{logo}" width="440">
        </div>
        """,
        unsafe_allow_html=True,
    )




    # ---------------- TITLE ----------------
    st.markdown('<div class="login-title">Welcome to Clustr</div>', unsafe_allow_html=True)

    # ---------------- SUBTITLE ----------------
    st.markdown('<div class="login-sub">Smart bundling optimizer for your business</div>',
                unsafe_allow_html=True)

    # ---------------- LOGIN CARD ----------------
    st.markdown('<div class="login-card">', unsafe_allow_html=True)

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

    st.markdown("</div>", unsafe_allow_html=True)  # end card
    st.markdown("</div>", unsafe_allow_html=True)  # end wrapper
