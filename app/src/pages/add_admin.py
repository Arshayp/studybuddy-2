import streamlit as st
from modules.nav import setup_page
import requests # Placeholder for potential future API calls

# Page Configuration
st.set_page_config(
    page_title="StudyBuddy - Add Admin",
    page_icon="🛡️",
    layout="wide"
)

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
    password = st.text_input("Password", type="password")
    
    submitted = st.form_submit_button("Create Admin")
    
    if submitted:
        if not name or not email or not password:
            st.error("Please fill in all fields.")
        else:
            # Placeholder for backend API call to create admin
            st.success(f"Admin '{name}' ({email}) creation request submitted (Placeholder).")
            # Optionally clear form or navigate away

# Button to go back to admin dashboard
if st.button("Back to Admin Dashboard"):
    st.switch_page("pages/admin_dashboard.py") 