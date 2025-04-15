import streamlit as st
from modules.nav import setup_page
import requests # Make sure requests is imported
import json # For handling JSON data

# Page Configuration
st.set_page_config(
    page_title="StudyBuddy - Add Admin",
    page_icon="🛡️",
    layout="wide"
)

# --- Backend API URL --- (Use Docker service name)
API_URL = "http://api:4000" # Flask service name 'api' and internal port 4000

# Setup: Theme, Auth, Sidebar (Ensure user is admin)
# Note: Add proper admin check logic here later
is_admin_user = st.session_state.get('user', {}).get('is_admin', False) # Placeholder

# Uncomment this when admin role check is properly implemented
# if not is_admin_user:
#     st.error("You do not have permission to access this page.")
#     st.stop()

setup_page("Add Admin") # Ensures sidebar and basic auth check

# --- Page Content ---
st.title("Add New Admin")

with st.form("add_admin_form"):
    st.subheader("Enter New Admin Details")
    name = st.text_input("Name")
    email = st.text_input("Email")
    # Collect Role instead of Password, as per backend schema
    role = st.text_input("Role (e.g., system administrator, content manager)") 
    
    submitted = st.form_submit_button("Create Admin")
    
    if submitted:
        # Update validation check
        if not name or not email or not role:
            st.error("Please fill in Name, Email, and Role.")
        else:
            # Prepare data for API
            admin_data = {
                "name": name,
                "role": role,
                "email": email
            }
            try:
                # Send POST request to backend
                response = requests.post(f"{API_URL}/admin/admins", json=admin_data)
                response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
                
                # Handle success
                result = response.json()
                st.success(result.get("message", "Admin created successfully!") + f" (ID: {result.get('adminid', 'N/A')})")
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