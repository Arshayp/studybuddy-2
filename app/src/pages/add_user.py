import streamlit as st
from modules.nav import setup_page
import requests # Make sure requests is imported
import json # For handling JSON data

# Page Configuration
st.set_page_config(
    page_title="StudyBuddy - Add User",
    page_icon="👤",
    layout="wide"
)

# --- Backend API URL --- (Use Docker service name)
API_URL = "http://api:4000" # Flask service name 'api' and internal port 4000

# Setup: Theme, Auth, Sidebar (Ensure user is admin)
# Note: Add proper admin check logic here later
is_admin = st.session_state.get('user', {}).get('is_admin', False) # Placeholder

# Uncomment this when admin role check is properly implemented
# if not is_admin:
#     st.error("You do not have permission to access this page.")
#     st.stop()

setup_page("Add User") # Ensures sidebar and basic auth check

# --- Page Content ---
st.title("Add New User")

with st.form("add_user_form"):
    st.subheader("Enter New User Details")
    name = st.text_input("Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    # Add other fields as necessary (e.g., role selection)
    
    submitted = st.form_submit_button("Create User")
    
    if submitted:
        if not name or not email or not password:
            st.error("Please fill in all fields.")
        else:
            # Prepare data for API
            user_data = {
                "name": name,
                "email": email,
                "password": password
            }
            try:
                # Send POST request to backend
                response = requests.post(f"{API_URL}/admin/users", json=user_data)
                response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
                
                # Handle success
                result = response.json()
                st.success(result.get("message", "User created successfully!") + f" (ID: {result.get('userid', 'N/A')})")
                # Consider clearing the form here if desired

            except requests.exceptions.RequestException as e:
                # Handle connection errors or bad responses
                st.error(f"API request failed: {e}")
                try:
                    # Try to parse error message from response if possible
                    error_details = response.json()
                    st.error(f"Backend error: {error_details.get('error', 'Unknown error')}")
                except (json.JSONDecodeError, NameError, AttributeError): # Handle cases where response isn't JSON or response object doesn't exist
                    st.error("Could not parse error details from backend response.")
            except Exception as e:
                 st.error(f"An unexpected error occurred: {e}")

# Button to go back to admin dashboard
if st.button("Back to Admin Dashboard"):
    st.switch_page("pages/admin_dashboard.py") 