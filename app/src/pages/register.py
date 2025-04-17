# naman
import streamlit as st
import requests # Import requests library bruh this is why it was not working
from modules.nav import apply_basic_theme

API_BASE_URL = "http://web-api:4000" # Use Docker service name

# --- Helper function to call registration API ---
def register_user_api(name, email, password, major=None, learning_style=None, availability=None):
    """Calls the backend API to register a new user."""
    register_url = f"{API_BASE_URL}/login" # POST /login handles registration
    payload = {
        "name": name,
        "email": email,
        "password": password,
        "major": major,
        "learning_style": learning_style,
        "availability": availability
    }
    try:
        response = requests.post(register_url, json=payload)
        response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
        return response.json(), None # Return success data
    except requests.exceptions.RequestException as e:
        # Handle connection errors or non-JSON error responses
        error_msg = str(e)
        try: # Attempt to get error detail from JSON response if available
            error_detail = response.json().get("error", response.text) if response.content else response.reason
            error_msg = f"API Error ({response.status_code}): {error_detail}"
        except: 
            pass 
        return None, error_msg
    except Exception as e:
        return None, f"An unexpected error occurred: {str(e)}"


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
                # Call the backend API to register the user
                result, error = register_user_api(
                    name, email, password, 
                    major if major else None, # Pass None if optional fields are empty
                    learning_style if learning_style else None,
                    availability if availability else None
                )
                
                if error:
                    st.error(f"Registration failed: {error}")
                else:
                    # Show success message from API response
                    st.success(result.get("message", "Account created successfully!"))
                    st.info("You can now log in using your credentials.")
                    
                    # Button to navigate to login (already existed, ensure it's visible)
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