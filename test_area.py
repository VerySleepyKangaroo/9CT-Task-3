import streamlit as st

# ------------------------
# Session State Defaults
# ------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# ------------------------
# Top Bar with Login Button
# ------------------------
col1, col2 = st.columns([6, 1])  # More space on left for title
with col2:
    if not st.session_state.logged_in:
        if st.button("Login", use_container_width=True):
            st.session_state.show_login = True
    else:
        if st.button("Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.show_login = False
            st.rerun()

# ------------------------
# Centered Title
# ------------------------
st.markdown(
    """
    <div style='text-align: center; padding-top: 50px;'>
        <h1>🌏 Climate & Emissions Dashboard</h1>
        <p>Compare average temperatures with emissions data for Australian states</p>
    </div>
    """,
    unsafe_allow_html=True
)

# ------------------------
# Optional Login Form Popup
# ------------------------
if st.session_state.get("show_login", False) and not st.session_state.logged_in:
    st.write("---")
    st.subheader("Sign In")
    username = st.text_input("Username")
    pwd = st.text_input("Passcode", type="password")

    if st.button("Sign in", use_container_width=True):
        if username == "Pranav" and pwd == "Pranav@GosfordHS1234":
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.show_login = False
            st.success(f"Welcome, {username}!")
            st.rerun()
        else:
            st.error("Incorrect username or password")

# ------------------------
# Show data if logged in
# ------------------------
if st.session_state.logged_in:
    st.info(f"Logged in as {st.session_state.username}")
    if st.button("View Climate Data and Emissions Data", use_container_width=True):
        # Place your full NSW/WA/VIC/QLD/ACT data display code here
        st.write("🔍 Data visualisation loading...")