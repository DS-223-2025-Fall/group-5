import streamlit as st


def settings_screen():
    st.markdown('<h1 style="margin-bottom:0.3rem;">Settings</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p style="color:#64748b;margin-bottom:1.3rem;">'
        'Configure how bundle recommendations are generated.'
        '</p>',
        unsafe_allow_html=True,
    )

    if "settings" not in st.session_state:
        st.session_state.settings = {
            "username": "Demo User",
            "theme": "Light",
            "min_support": 0.01,
            "min_confidence": 0.0,
        }

    s = st.session_state.settings

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Recommendation Settings")

    s["username"] = st.text_input("Display name", value=s["username"])

    col1, col2 = st.columns(2)
    with col1:
        s["min_support"] = st.slider(
            "Minimum support (fraction)",
            0.0,
            0.2,
            float(s["min_support"]),
            step=0.005,
        )
    with col2:
        s["min_confidence"] = st.slider(
            "Minimum confidence (0–1, used to filter display)",
            0.0,
            1.0,
            float(s["min_confidence"]),
            step=0.05,
        )

    theme = st.selectbox("Theme (visual only)", ["Light", "Dark"], index=["Light", "Dark"].index(s["theme"]))
    s["theme"] = theme

    if st.button("Save settings"):
        st.success("Settings saved (stored in session).")

    st.markdown("</div>", unsafe_allow_html=True)
