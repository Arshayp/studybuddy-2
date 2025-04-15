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

# Uncomment this when admin role check is properly implemented
# if not is_admin:
#     st.error("You do not have permission to access this page.")
#     st.stop()

setup_page("Admin Dashboard") 

# --- Page Content ---
st.title("Admin Dashboard")

# Create tabs
tab1, tab2 = st.tabs(["User Management", "Admin Management"])

with tab1:
    st.header("User Management")

    # Example hardcoded user data (non-admins)
    users = [
        {"id": 1, "name": "Alice", "email": "alice@example.com", "role": "student"},
        {"id": 2, "name": "Bob", "email": "bob@example.com", "role": "student"},
    ]

    if users:
        st.write("Current Users:")
        # Header row
        col1, col2, col3, col4 = st.columns([1, 2, 3, 2])
        with col1:
            st.write("**ID**")
        with col2:
            st.write("**Name**")
        with col3:
            st.write("**Email**")
        with col4:
            st.write("**Actions**")

        # User rows
        for user in users:
            col1, col2, col3, col4 = st.columns([1, 2, 3, 2])
            with col1:
                st.write(user['id'])
            with col2:
                st.write(user['name'])
            with col3:
                st.write(user['email'])
            with col4:
                # Add buttons for actions like Edit, Delete later
                st.button("Edit", key=f"edit_user_{user['id']}") 
                st.button("Delete", key=f"delete_user_{user['id']}")
    else:
        st.write("No users found.")

    # Use st.switch_page to navigate
    if st.button("Add New User", key="add_user_nav"):
        st.switch_page("pages/add_user.py")
    # Add functionality for adding users later

with tab2:
    st.header("Admin Management")

    # Example hardcoded admin data
    admins = [
        {"id": 3, "name": "Admin User", "email": "admin@example.com", "role": "admin"},
        # Add more admins if needed
    ]

    if admins:
        st.write("Current Admins:")
        # Header row
        col1, col2, col3, col4 = st.columns([1, 2, 3, 2])
        with col1:
            st.write("**ID**")
        with col2:
            st.write("**Name**")
        with col3:
            st.write("**Email**")
        with col4:
            st.write("**Actions**")
        
        # Admin rows
        for admin in admins:
            col1, col2, col3, col4 = st.columns([1, 2, 3, 2])
            with col1:
                st.write(admin['id'])
            with col2:
                st.write(admin['name'])
            with col3:
                st.write(admin['email'])
            with col4:
                # Add buttons for actions like Edit, Delete later
                # Make sure keys are unique across tabs
                st.button("Edit", key=f"edit_admin_{admin['id']}") 
                st.button("Delete", key=f"delete_admin_{admin['id']}")
    else:
        st.write("No admins found.")

    # Use st.switch_page to navigate
    if st.button("Add New Admin", key="add_admin_nav"):
        st.switch_page("pages/add_admin.py")
    # Add functionality for adding admins later
