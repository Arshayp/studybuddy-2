import streamlit as st
from modules.nav import setup_page

# Page Configuration
st.set_page_config(
    page_title="StudyBuddy - Admin Dashboard",
    page_icon="🔒",
    layout="wide"
)

# Setup: Theme, Auth, Sidebar (Check if user is admin)
# Note: Add admin check logic here later
is_admin = st.session_state.get('user', {}).get('is_admin', False) # Placeholder for admin check

#if not is_admin:
#    st.error("You do not have permission to access this page.")
#    st.stop()

setup_page("Admin Dashboard") 

# --- Page Content ---
st.title("Admin Dashboard")
st.header("User Management")

# Example hardcoded user data
users = [
    {"id": 1, "name": "Alice", "email": "alice@example.com", "role": "student"},
    {"id": 2, "name": "Bob", "email": "bob@example.com", "role": "student"},
    {"id": 3, "name": "Admin User", "email": "admin@example.com", "role": "admin"},
]

if users:
    st.write("Current Users:")
    for user in users:
        col1, col2, col3, col4 = st.columns([1, 2, 3, 1])
        with col1:
            st.write(user['id'])
        with col2:
            st.write(user['name'])
        with col3:
            st.write(user['email'])
        with col4:
            # Add buttons for actions like Edit, Delete later
            st.button("Edit", key=f"edit_{user['id']}") 
            st.button("Delete", key=f"delete_{user['id']}")

else:
    st.write("No users found.")

st.button("Add New User")
# Add functionality for adding users later
