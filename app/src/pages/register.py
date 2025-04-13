# naman
import streamlit as st
from modules.nav import apply_basic_theme

def register_form():
    """Displays the registration form for new users."""
    st.title("Create a StudyBuddy Account")
    
    with st.form("register_form"):
        st.write("Register for a new account")
        name = st.text_input("Full Name", placeholder="Your Name")
        email = st.text_input("Email", placeholder="your.email@example.com")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        
        # Optional user info from database schema
        col1, col2 = st.columns(2)
        with col1:
            major = st.text_input("Major (Optional)", placeholder="e.g., Computer Science")
        with col2:
            learning_style = st.text_input("Learning Style (Optional)", placeholder="e.g., Visual")
        
        availability = st.text_input("Availability (Optional)", placeholder="e.g., Evenings and weekends")
        
        submitted = st.form_submit_button("Register")
        
        if submitted:
            if not (name and email and password and confirm_password):
                st.error("Please fill out all required fields.")
            elif password != confirm_password:
                st.error("Passwords do not match.")
            else:
                # This would normally connect to your backend API
                # For now, just show a success message
                st.success("Account created successfully! You can now log in.")
                
                # Link to login page
                if st.button("Go to Login"):
                    st.switch_page("pages/login.py")

# Return to login option
def show_login_option():
    st.write("Already have an account?")
    if st.button("Log In"):
        st.switch_page("pages/login.py")

# --- Main Script Execution ---
# Set page config (must be first Streamlit call)
st.set_page_config(
    page_title="StudyBuddy Registration",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Apply basic theme (hide footer/menu)
apply_basic_theme()

# Simple page layout
register_form()
st.divider()
show_login_option() 