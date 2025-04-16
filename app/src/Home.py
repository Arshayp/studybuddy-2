# naman
##################################################
# Main entry point for the StudyBuddy application.
# Handles routing based on login status and redirects
# logged-in users to the main dashboard page.
##################################################

import streamlit as st
# No longer need setup_page here
# from modules.nav import setup_page

# Set page config first
st.set_page_config(
    page_title="StudyBuddy", # Simplified title for the landing/routing page
    page_icon="📚",
    layout="wide"
)

# Initialize session state if keys don't exist
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user" not in st.session_state:
    st.session_state.user = {}

# --- Page Logic ---
if not st.session_state.logged_in:
    # If not logged in, show login page
    st.switch_page("pages/login.py")
    # No need to stop here, switch_page handles it
else:
    # If logged in, immediately switch to the main dashboard page
    st.switch_page("pages/dashboard.py")
    # No need to stop here

# --- Removed Dashboard Content ---
# The code previously here (headers, columns, profile summary, etc.)
# has been removed as this page now only handles routing.
# The actual dashboard content resides in pages/dashboard.py.