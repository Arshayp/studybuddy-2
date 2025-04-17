# naman
import streamlit as st
import requests # Import requests
from datetime import datetime
from modules.nav import setup_page

# API_BASE_URL = "http://127.0.0.1:5000" # Adjust if backend runs elsewhere
API_BASE_URL = "http://web-api:4000" # Use Docker service name

# Page Configuration
st.set_page_config(
    page_title="StudyBuddy - Dashboard",
    page_icon="📊",
    layout="wide"
)

# Set current page in session state
st.session_state.page = 'dashboard'

# Setup: Theme, Auth, Sidebar
setup_page("Dashboard") 

# --- Helper function to fetch user resources (GET request) ---
def get_user_resources(user_id):
    if not user_id:
        return None, "User ID not provided."
    resources_url = f"{API_BASE_URL}/users/{user_id}/resources" # Updated URL
    try:
        response = requests.get(resources_url)
        if response.status_code == 200:
            return response.json(), None # Return data, no error
        else:
            return None, f"API Error: {response.status_code} - {response.text}"
    except requests.exceptions.RequestException as e:
        return None, f"Connection Error: {e}"

# --- Helper function to fetch potential matches (GET request) ---
def get_potential_matches(user_id):
    """Fetches potential matches for the user."""
    if not user_id:
        return None, "User ID not provided."
    # Uses the new endpoint GET /users/<user_id>/potential-matches
    matches_url = f"{API_BASE_URL}/users/{user_id}/potential-matches"
    try:
        response = requests.get(matches_url)
        response.raise_for_status()
        return response.json(), None
    except requests.exceptions.RequestException as e:
        return None, str(e)
    except Exception as e:
        return None, f"An unexpected error occurred: {str(e)}"

# --- Helper function to fetch user's groups (GET request) ---
def get_user_groups(user_id):
    """Fetches groups the user is a member of."""
    if not user_id:
        return None, "User ID not provided."
    # This now uses the new endpoint in the user_profile blueprint
    groups_url = f"{API_BASE_URL}/users/{user_id}/groups" 
    try:
        response = requests.get(groups_url)
        response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
        return response.json(), None
    except requests.exceptions.RequestException as e:
        return None, str(e)
    except Exception as e:
        return None, f"An unexpected error occurred: {str(e)}"
    # Removed the previous commented-out code and return [] statement

# --- Helper function to add a resource (POST request) ---
def add_user_resource(user_id, link, resource_type):
    """Adds a new resource for the user."""
    if not all([user_id, link, resource_type]):
        return None, "Missing user_id, link, or type."
        
    add_url = f"{API_BASE_URL}/users/{user_id}/resources"
    payload = {"link": link, "type": resource_type}
    try:
        response = requests.post(add_url, json=payload)
        response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
        return response.json(), None # Return success/info message
    except requests.exceptions.RequestException as e:
        # Handle potential non-JSON error responses or connection issues
        error_msg = str(e)
        try: # Attempt to get error detail from JSON response if available
            error_detail = response.json().get("error", response.text) if response.content else response.reason
            error_msg = f"API Error ({response.status_code}): {error_detail}"
        except: # If response wasn't JSON or other error
            pass 
        return None, error_msg
    except Exception as e:
        return None, f"An unexpected error occurred: {str(e)}"

# --- Page Content ---
st.title("StudyBuddy Dashboard")

left_col, right_col = st.columns(2)

with left_col:
    st.subheader("Your Study Groups")
    # --- Fetch and display user's study groups from API ---
    user_id = st.session_state.user.get('id')
    groups, error = get_user_groups(user_id)

    if error:
        st.error(f"Could not load study groups: {error}")
    elif groups: # Check if the list is not empty
        for group in groups:
            # API returns groupid, group_name
            with st.expander(f"**{group.get('group_name', 'Unnamed Group')}**"):
                st.write(f"Group ID: {group.get('groupid', 'N/A')}")
                # Add actions like 'View Group' or 'Leave Group' later
                st.button("View Details (Not implemented)", key=f"view_group_{group.get('groupid')}")
    else:
        st.write("You are not currently in any study groups.")
    # --- End of study groups section ---
    
    st.subheader("Study Resources")
    # --- Fetch and display resources from API ---
    user_id = st.session_state.user.get('id')
    resources, error = get_user_resources(user_id)
    
    if error:
        st.error(f"Could not load resources: {error}")
    elif resources: # Check if the list is not empty
        for resource in resources:
            # Adjust keys based on actual API response columns (resourceid, resource_link, resource_type)
            with st.expander(f"**{resource.get('resource_link', 'Unnamed Resource')}**"):
                st.write(f"Type: {resource.get('resource_type', 'N/A')}")
                # Use link_button for external links
                st.link_button("Go to Resource", url=resource.get('resource_link', '#')) 
    else: # API call was successful but returned empty list or None
        st.write("No study resources found.")
        
    st.divider()
    # --- Add Resource Form ---
    with st.expander("Add a New Resource"):
        with st.form("add_resource_form", clear_on_submit=True):
            new_link = st.text_input("Resource Link (URL)")
            new_type = st.text_input("Resource Type (e.g., Tutorial, Notes, Video)")
            submitted = st.form_submit_button("Add Resource")
            if submitted:
                if new_link and new_type: # Basic validation
                    user_id = st.session_state.user.get('id')
                    result, error = add_user_resource(user_id, new_link, new_type)
                    if error:
                        st.error(f"Failed to add resource: {error}")
                    else:
                        st.success(result.get("message", "Resource added successfully!"))
                        st.rerun() # Rerun to show the new resource in the list above
                else:
                    st.warning("Please provide both a link and a type.")
    # --- End of resources section ---

with right_col:
    st.subheader("Profile Summary")
    user_info = st.session_state.get('user', {})
    st.write(f"Name: {user_info.get('name', 'N/A')}")
    st.write(f"Email: {user_info.get('email', 'N/A')}") # Display email too?
    
    if st.button("Edit Profile & Settings", use_container_width=True):
        st.switch_page("pages/profile.py")
    
    st.subheader("Potential Study Matches")
    # --- Fetch and display potential matches from API ---
    user_id = st.session_state.user.get('id')
    matches, error = get_potential_matches(user_id)
    
    if error:
        st.error(f"Could not load potential matches: {error}")
    elif matches: # Check if the list is not empty
        st.write("Here are some potential study partners:")
        for match in matches:
            # Adjust keys based on API response (userid, name, email, major, etc.)
            with st.expander(f"**{match.get('name', 'Unknown User')}** - Major: {match.get('major', 'N/A')}"):
                st.write(f"Email: {match.get('email', 'N/A')}")
                st.write(f"Learning Style: {match.get('learning_style', 'N/A')}")
                st.write(f"Availability: {match.get('availability', 'N/A')}")
                # Add a button or action later if needed
                st.button("Connect (Not implemented)", key=f"connect_{match.get('userid')}")
    else: # API call successful but returned empty list or None
        st.write("No potential matches found at this time.")
    # --- End of matches section --- 