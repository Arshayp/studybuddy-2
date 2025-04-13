# naman
import streamlit as st
from pathlib import Path
from modules.nav import apply_basic_theme # Use simplified theme

def login_form():
    """Displays the login form and handles hardcoded demo login."""
    st.title("StudyBuddy Login")
    
    with st.form("login_form"):
        st.write("Log in to your account (Use demo credentials)")
        email = st.text_input("Email", placeholder="demo@example.com")
        password = st.text_input("Password", type="password", placeholder="password")
        
        submitted = st.form_submit_button("Log In")
        
        if submitted:
            if email and password:
                # Hardcoded demo authentication ONLY
                if email == "demo@example.com" and password == "password":
                    st.session_state.logged_in = True
                    # Save minimal user info
                    st.session_state.user = {"email": email, "name": "Demo User"}
                    st.switch_page("Home.py") 
                else:
                    st.error("Invalid email or password. Please use demo credentials.")
            else:
                st.error("Please enter email and password.")
    
    # Removed Create Account button

# Removed register_form function entirely

# Removed reset_password_form function entirely

# --- Main Script Execution ---
# Set page config (must be first Streamlit call)
st.set_page_config(
    page_title="StudyBuddy Login",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Apply basic theme (hide footer/menu)
apply_basic_theme()

# Initialize session state if needed
if "page" not in st.session_state: # Although 'page' is no longer used for routing here, keep for potential future use?
    st.session_state.page = "login"
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Simple Routing/Display Logic
if st.session_state.logged_in:
    # If already logged in, go to dashboard
    st.switch_page("Home.py")
    st.stop()
else:
    # Only show login form if not logged in
    login_form()