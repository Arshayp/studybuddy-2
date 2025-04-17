# naman
import streamlit as st
import requests
from pathlib import Path
from modules.nav import apply_basic_theme # Use simplified theme

# Define the backend API endpoint URL
API_LOGIN_URL = "http://web-api:4000/login"  # Changed to use Docker service name

def login_form():
    """Displays the login form and handles login attempts via API."""
    st.title("StudyBuddy Login")
    
    with st.form("login_form"):
        st.write("Log in to your account")
        email = st.text_input("Email", placeholder="your.email@example.com")
        password = st.text_input("Password", type="password")
        
        submitted = st.form_submit_button("Log In")
        
        if submitted:
            if not (email and password):
                st.error("Please enter email and password.")
                return

            # Try logging in via API
            try:
                payload = {"email": email, "password": password}
                response = requests.put(API_LOGIN_URL, json=payload)
                
                if response.status_code == 200:
                    user_data = response.json()
                    # Get the user ID from the response
                    user_id = user_data.get('user_id')
                    
                    if not user_id:
                        st.error("User ID not found in response")
                        return
                        
                    st.session_state.logged_in = True
                    st.session_state.authenticated = True
                    st.session_state.role = "student"
                    st.session_state.user = {
                        "email": email,
                        "name": email.split('@')[0],  # Use email prefix as name if not provided
                        "id": user_id  # Changed from user_id to id to match study_groups.py
                    }
                    st.switch_page("Home.py")
                else:
                    st.error("Invalid email or password.")
                    
            except requests.exceptions.RequestException as e:
                st.error(f"Could not connect to login service: {e}")
                return 
            except Exception as e:
                st.error("An unexpected error occurred during login.")
                return
    
    # Add Create Account button
    st.write("Don't have an account?")
    if st.button("Create Account"):
        st.switch_page("pages/register.py")

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
if "page" not in st.session_state:
    st.session_state.page = "login"
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user" not in st.session_state:
    st.session_state.user = {}

# Simple Routing/Display Logic
if st.session_state.logged_in:
    # If already logged in, go to dashboard
    st.switch_page("Home.py")
    st.stop()
else:
    # Only show login form if not logged in
    login_form()