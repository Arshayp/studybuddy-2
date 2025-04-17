import streamlit as st
from modules.nav import setup_page
import requests
import json # Import json for potential error parsing

# Page Configuration
st.set_page_config(
    page_title="StudyBuddy - Admin Dashboard",
    page_icon="🔒",
    layout="wide"
)

# --- Backend API URL --- (Use Docker service name)
API_URL = "http://api:4000" # Flask service name 'api' and internal port 4000

# --- Initialize session state for delete confirmation --- 
if 'item_to_delete' not in st.session_state:
    st.session_state.item_to_delete = None
if 'delete_type' not in st.session_state:
    st.session_state.delete_type = None
# Add state for editing
if 'item_to_edit' not in st.session_state:
    st.session_state.item_to_edit = None 
if 'edit_type' not in st.session_state:
    st.session_state.edit_type = None

# Setup: Theme, Auth, Sidebar (Check if user is admin)
# Note: Add admin check logic here later
is_admin = st.session_state.get('user', {}).get('is_admin', False) # Placeholder for admin check

# Uncomment this when admin role check is properly implemented
# if not is_admin:
#     st.error("You do not have permission to access this page.")
#     st.stop()

setup_page("Admin Dashboard") 

# --- Helper functions to fetch data --- 
@st.cache_data(ttl=60) # Cache data for 60 seconds
def fetch_users():
    try:
        response = requests.get(f"{API_URL}/admin/users")
        response.raise_for_status()
        return response.json().get('users', []), None # Return data, no error
    except requests.exceptions.RequestException as e:
        error_msg = f"API request failed: {e}"
        try: 
            error_details = response.json()
            error_msg += f" Backend error: {error_details.get('error', 'Unknown')}"
        except: pass
        return None, error_msg
    except Exception as e:
        return None, f"An unexpected error occurred: {e}"

@st.cache_data(ttl=60) # Cache data for 60 seconds
def fetch_admins():
    try:
        response = requests.get(f"{API_URL}/admin/all")
        response.raise_for_status()
        return response.json().get('admins', []), None # Return data, no error
    except requests.exceptions.RequestException as e:
        error_msg = f"API request failed: {e}"
        try: 
            error_details = response.json()
            error_msg += f" Backend error: {error_details.get('error', 'Unknown')}"
        except: pass
        return None, error_msg
    except Exception as e:
        return None, f"An unexpected error occurred: {e}"

# --- Functions to fetch counts ---
@st.cache_data(ttl=60)
def fetch_user_count():
    try:
        response = requests.get(f"{API_URL}/admin/users/count")
        response.raise_for_status()
        return response.json().get('count', 0), None # Return count, no error
    except requests.exceptions.RequestException as e:
        error_msg = f"API request failed: {e}"
        try: error_details = response.json(); error_msg += f" Backend error: {error_details.get('error', 'Unknown')}"
        except: pass
        return None, error_msg
    except Exception as e:
        return None, f"An unexpected error occurred fetching user count: {e}"

@st.cache_data(ttl=60)
def fetch_admin_count():
    try:
        response = requests.get(f"{API_URL}/admin/admins/count")
        response.raise_for_status()
        return response.json().get('count', 0), None # Return count, no error
    except requests.exceptions.RequestException as e:
        error_msg = f"API request failed: {e}"
        try: error_details = response.json(); error_msg += f" Backend error: {error_details.get('error', 'Unknown')}"
        except: pass
        return None, error_msg
    except Exception as e:
        return None, f"An unexpected error occurred fetching admin count: {e}"

# --- Function to handle actual deletion API call ---
def perform_delete(item_id, delete_type):
    if delete_type == 'user':
        url = f"{API_URL}/admin/users/{item_id}"
    elif delete_type == 'admin':
        url = f"{API_URL}/admin/admins/{item_id}"
    else:
        st.error("Invalid delete type.")
        return
        
    try:
        response = requests.delete(url)
        response.raise_for_status()
        st.success(response.json().get('message', f"{delete_type.capitalize()} deleted successfully."))
        st.cache_data.clear()
        st.session_state.item_to_delete = None
        st.session_state.delete_type = None
        st.rerun()
    except requests.exceptions.RequestException as e:
        st.error(f"API request failed: {e}")
        try: error_details = response.json(); st.error(f"Backend error: {error_details.get('error', 'Unknown error')}")
        except: st.error("Could not parse error details.")
    except Exception as e:
        st.error(f"An unexpected error occurred during deletion: {e}")

# --- Function to handle update API call ---
def perform_update(item_id, update_type, update_data):
    if update_type == 'user':
        url = f"{API_URL}/admin/users/{item_id}"
    elif update_type == 'admin':
        url = f"{API_URL}/admin/admins/{item_id}"
    else:
        st.error("Invalid update type.")
        return False # Indicate failure
        
    try:
        response = requests.put(url, json=update_data)
        response.raise_for_status()
        st.success(response.json().get('message', f"{update_type.capitalize()} updated successfully."))
        st.cache_data.clear() 
        return True # Indicate success
    except requests.exceptions.RequestException as e:
        st.error(f"API request failed: {e}")
        try: error_details = response.json(); st.error(f"Backend error: {error_details.get('error', 'Unknown error')}")
        except: st.error("Could not parse error details.")
        return False # Indicate failure
    except Exception as e:
        st.error(f"An unexpected error occurred during update: {e}")
        return False # Indicate failure

# --- Edit Dialog Function ---
@st.dialog("Edit Item")
def show_edit_dialog(item, item_type):
    st.subheader(f"Editing {item_type.capitalize()} ID: {item.get('userid' if item_type == 'user' else 'adminid')}")
    
    # Form for editing
    with st.form(key=f"edit_form_{item_type}_{item.get('userid' if item_type == 'user' else 'adminid')}"): # Use simpler key
        new_data = {}
        if item_type == 'user':
            new_data['name'] = st.text_input("Name", value=item.get('name', ''))
            new_data['email'] = st.text_input("Email", value=item.get('email', ''))
            new_data['major'] = st.text_input("Major", value=item.get('major', ''))
            new_data['learning_style'] = st.text_input("Learning Style", value=item.get('learning_style', ''))
            new_data['availability'] = st.text_input("Availability", value=item.get('availability', ''))
        elif item_type == 'admin':
            new_data['name'] = st.text_input("Name", value=item.get('name', ''))
            new_data['email'] = st.text_input("Email", value=item.get('email', ''))
            new_data['role'] = st.text_input("Role", value=item.get('role', ''))
        
        submitted = st.form_submit_button("Save Changes")
        if submitted:
            item_id = item.get('userid' if item_type == 'user' else 'adminid')
            update_payload = {k: v for k, v in new_data.items() if v is not None and v != ''} 
            if perform_update(item_id, item_type, update_payload):
                st.session_state.item_to_edit = None 
                st.session_state.edit_type = None
                st.rerun()
                
    # Add Cancel button *outside* the form
    if st.button("Cancel", key=f"cancel_edit_{item_type}_{item.get('userid' if item_type == 'user' else 'adminid')}"):
        st.session_state.item_to_edit = None
        st.session_state.edit_type = None
        st.rerun()

# --- Page Content ---
st.title("Admin Dashboard")

# --- Display Count Metrics --- 
st.subheader("Platform Overview")
user_count, user_err = fetch_user_count()
admin_count, admin_err = fetch_admin_count()

col1, col2, col3 = st.columns(3) # Use 3 columns for spacing
with col1:
    if user_err:
        st.metric(label="Total Users", value="Error")
        st.error(user_err, icon="🚨")
    elif user_count is None:
        st.metric(label="Total Users", value="Loading...")
    else:
        st.metric(label="Total Users", value=user_count)

with col2:
    if admin_err:
        st.metric(label="Total Admins", value="Error")
        st.error(admin_err, icon="🚨")
    elif admin_count is None:
        st.metric(label="Total Admins", value="Loading...")
    else:
        st.metric(label="Total Admins", value=admin_count)
st.divider() # Add a divider before the tabs

# --- Display Confirmation Dialog for Deletion --- 
if st.session_state.item_to_delete is not None:
    item_id = st.session_state.item_to_delete
    item_type = st.session_state.delete_type
    st.warning(f"Are you sure you want to delete {item_type} ID: {item_id}?", icon="⚠️")
    col_confirm, col_cancel = st.columns(2)
    with col_confirm:
        if st.button("Confirm Delete", key=f"confirm_delete_{item_type}_{item_id}", use_container_width=True):
            perform_delete(item_id, item_type)
    with col_cancel:
        if st.button("Cancel", key=f"cancel_delete_{item_type}_{item_id}", use_container_width=True):
            st.session_state.item_to_delete = None
            st.session_state.delete_type = None
            st.rerun()

# --- Display Edit Dialog --- 
if st.session_state.item_to_edit is not None:
    show_edit_dialog(st.session_state.item_to_edit, st.session_state.edit_type)

# Create tabs
tab1, tab2 = st.tabs(["User Management", "Admin Management"])

# --- User Management Tab --- 
with tab1:
    st.header("User Management")
    users, error = fetch_users()

    if error: st.error(f"Could not load users: {error}")
    elif users is None: st.info("Loading user data...") 
    elif not users: st.write("No users found.")
    else:
        st.write("Current Users:")
        cols = st.columns([1, 2, 3, 1, 1, 1, 1]) # ID, Name, Email, Major, Flagged, Actions
        headers = ["ID", "Name", "Email", "Major",  "", ""] 
        for i, header in enumerate(headers): cols[i].write(f"**{header}**")

        for user in users:
            user_id = user.get('userid')
            is_flagged = user.get('is_flagged', False) # Get flag status
            
            cols = st.columns([1, 2, 3, 1, 1, 1, 1]) 
            cols[0].write(user_id)
            cols[1].write(user.get('name', 'N/A'))
            cols[2].write(user.get('email', 'N/A'))
            cols[3].write(user.get('major', 'N/A')) 
            
            
            # --- Action Buttons --- 
            # Edit Button
            edit_key = f"edit_user_{user_id}"
            if cols[5].button("📝", key=edit_key, help="Edit User"):
                st.session_state.item_to_edit = user 
                st.session_state.edit_type = 'user'
                st.session_state.item_to_delete = None 
                st.session_state.delete_type = None
                st.rerun()
            
            # Delete Button
            delete_key = f"delete_user_{user_id}"
            if cols[5].button("🗑️", key=delete_key, help="Delete User"):
                st.session_state.item_to_delete = user_id
                st.session_state.delete_type = 'user'
                st.session_state.item_to_edit = None 
                st.session_state.edit_type = None
                st.rerun()

            # Flag/Unflag Button (Toggle Appearance + Frontend Message Only)
            flag_key = f"flag_user_{user_id}"
            flag_icon = "🏴‍☠️" if is_flagged else "🚩"
            flag_help = "Unflag User" if is_flagged else "Flag User"
            action_text = "Unflagged" if is_flagged else "Flagged"
            if cols[6].button(flag_icon, key=flag_key, help=flag_help):
                 st.success(f"User {user_id} {action_text} ")
    
    if st.button("Add New User", key="add_user_nav"): st.switch_page("pages/add_user.py")

# --- Admin Management Tab --- 
with tab2:
    st.header("Admin Management")
    admins, error = fetch_admins()
    
    if error: st.error(f"Could not load admins: {error}")
    elif admins is None: st.info("Loading admin data...")
    elif not admins: st.write("No admins found.")
    else:
        st.write("Current Admins:")
        cols = st.columns([1, 2, 3, 2, 2])
        headers = ["ID", "Name", "Email", "Role", "Actions"]
        for col, header in zip(cols, headers): col.write(f"**{header}**")
        
        for admin in admins:
            admin_id = admin.get('adminid')
            cols = st.columns([1, 2, 3, 2, 2])
            cols[0].write(admin_id)
            cols[1].write(admin.get('name', 'N/A'))
            cols[2].write(admin.get('email', 'N/A'))
            cols[3].write(admin.get('role', 'N/A'))
            with cols[4]: 
                edit_key = f"edit_admin_{admin_id}"
                if st.button("📝", key=edit_key, help="Edit Admin"):
                    st.session_state.item_to_edit = admin 
                    st.session_state.edit_type = 'admin'
                    st.session_state.item_to_delete = None 
                    st.session_state.delete_type = None
                    st.rerun()
                delete_key = f"delete_admin_{admin_id}"
                if st.button("🗑️", key=delete_key, help="Delete Admin"):
                    st.session_state.item_to_delete = admin_id
                    st.session_state.delete_type = 'admin'
                    st.session_state.item_to_edit = None 
                    st.session_state.edit_type = None
                    st.rerun()

    if st.button("Add New Admin", key="add_admin_nav"): st.switch_page("pages/add_admin.py")
