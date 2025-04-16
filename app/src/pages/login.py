# naman
import streamlit as st
import requests # Import requests library
# import logging # Removed logging import
from pathlib import Path
from modules.nav import apply_basic_theme # Use simplified theme

# Define the backend API endpoint URL
API_LOGIN_URL = "http://web-api:4000/login" 

def login_form():
    """Displays the login form and handles login attempts via API and fallback demo."""
    st.title("StudyBuddy Login")
    
    with st.form("login_form"):
        st.write("Log in to your account")
        email = st.text_input("Email", placeholder="your.email@example.com")
        password = st.text_input("Password", type="password")
        
        submitted = st.form_submit_button("Log In")
        
        login_successful = False
        if submitted:
            if not (email and password):
                st.error("Please enter email and password.")
                return # Stop processing if fields are empty

            # --- Try logging in via API first ---
            try:
                payload = {"email": email, "password": password}
                # logging.info(f"Attempting API login for: {email}") # Removed logging
                response = requests.put(API_LOGIN_URL, json=payload)
                
                if response.status_code == 200:
                    user_data = response.json() 
                    st.session_state.logged_in = True
                    # Store user info (adjust keys based on actual API response)
                    st.session_state.user = {
                        "email": email, 
                        "name": user_data.get('name', email), # Use email as fallback name
                        "id": user_data.get("user_id")
                    } 
                    st.success("Login successful!")
                    st.switch_page("pages/dashboard.py")
                    login_successful = True # Flag success
                else:
                    # Log non-200 responses for debugging if needed
                    # logging.warning(f"API Login Failed for {email}: {response.status_code} - {response.text}") # Removed logging
                    # Don't show API error directly to user, fall through to check demo
                    pass # Explicitly do nothing if API login fails, just fall through
                    
            except requests.exceptions.RequestException as e:
                st.error(f"Could not connect to login service: {e}")
                # Don't proceed if connection failed
                return 
            except Exception as e:
                # Catch other potential errors during API interaction
                # logging.error(f"Unexpected error during API login for {email}: {e}") # Removed logging
                st.error("An unexpected error occurred during login.")
                return

            # --- If API login didn't succeed, check hardcoded demo credentials ---
            if not login_successful and email == "demo@example.com" and password == "password":
                st.session_state.logged_in = True
                st.session_state.user = {"email": email, "name": "Demo User", "id": None} 
                st.success("Login successful using demo credentials!")
                st.switch_page("pages/dashboard.py")
                login_successful = True # Flag success
            
            # --- If neither API nor demo login worked, show error ---
            if not login_successful:
                 st.error("Invalid email or password.")

    # Add Create Account button
    st.write("Don't have an account?")
    if st.button("Create Account"):
        st.switch_page("pages/register.py")

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

# Initialize session state if needed
if "page" not in st.session_state:
    st.session_state.page = "login"
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# Simple Routing/Display Logic
if st.session_state.logged_in:
    # If already logged in, go to dashboard
    st.switch_page("pages/dashboard.py")
    st.stop()
else:
    # Only show login form if not logged in
    apply_basic_theme()
    login_form()