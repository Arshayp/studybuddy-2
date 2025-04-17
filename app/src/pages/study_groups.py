# naman
import streamlit as st
import requests # Import requests
from datetime import datetime # Keep for demo data
from modules.nav import setup_page

# API_BASE_URL = "http://127.0.0.1:5000"  # Adjust as necessary
API_BASE_URL = "http://web-api:4000" # Use Docker service name

# Page Config
st.set_page_config(
    page_title="StudyBuddy - Study Groups",
    page_icon="👥",
    layout="wide"
)

# Basic setup
setup_page("Study Groups")

# --- Helper function to fetch user's study groups (GET request) ---
def get_user_study_groups(user_id):
    """Fetches groups the user is a member of."""
    if not user_id:
        return None, "User ID not found."
    # Use the new endpoint GET /users/<user_id>/groups
    groups_url = f"{API_BASE_URL}/users/{user_id}/groups"
    try:
        response = requests.get(groups_url)
        response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
        return response.json(), None
    except requests.exceptions.RequestException as e:
        return None, str(e)
    except Exception as e:
        return None, f"An unexpected error occurred: {str(e)}"

# --- Helper function to fetch all available study groups (GET request) ---
def get_available_groups():
    # groups_url = f"{API_BASE_URL}/u/groups/find"
    groups_url = f"{API_BASE_URL}/groups/find" # Updated URL
    try:
        response = requests.get(groups_url)
        if response.status_code == 200:
            return response.json(), None # Return data, no error
        else:
            return None, f"API Error: {response.status_code} - {response.text}"
    except requests.exceptions.RequestException as e:
        return None, f"Connection Error: {e}"

# --- Helper function to create a study group (POST request) ---
def create_study_group(group_name, user_id):
    if not group_name:
        return None, "Group name cannot be empty."
        
    # create_url = f"{API_BASE_URL}/u/groups/create"
    create_url = f"{API_BASE_URL}/groups/create" # Updated URL
    payload = {"group_name": group_name, "user_id": user_id}
    try:
        response = requests.post(create_url, json=payload)
        if response.status_code == 201: # Check for 201 Created status
            return response.json(), None # Return data, no error
        else:
            # Try to get error message from API response, otherwise use status/text
            error_detail = response.json().get("error", response.text) if response.content else response.reason
            return None, f"API Error ({response.status_code}): {error_detail}"
    except requests.exceptions.RequestException as e:
        return None, f"Connection Error: {e}"
    except Exception as e: # Catch other potential errors like JSON decoding
        return None, f"An unexpected error occurred: {str(e)}"

# --- Helper function to join a study group (POST request) ---
def join_study_group(group_id, user_id):
    if not group_id or not user_id:
        return None, "Missing group_id or user_id."
        
    join_url = f"{API_BASE_URL}/groups/{group_id}/join"
    payload = {"user_id": user_id}
    try:
        response = requests.post(join_url, json=payload)
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

st.title("Study Groups")

# Tabs for sections
my_groups_tab, find_groups_tab, create_group_tab = st.tabs(["My Groups", "Find Groups", "Create Group"])

with my_groups_tab:
    st.subheader("Your Study Groups")
    
    # --- Fetch and display user's study groups from API ---
    user_id = st.session_state.user.get('id') # Get user ID from session state
    groups, error = get_user_study_groups(user_id)
    
    if error:
        # Display error message
        st.error(f"Could not load your study groups: {error}")
        # Also display the specific warning if it's the disabled functionality message
        if "Functionality disabled" in error:
            st.warning(error)
    elif groups: # Check if the list is not empty
        for group in groups:
            # API returns groupid, group_name
            st.write(f"**{group.get('group_name', 'Unnamed Group')}**")
            # Simple action buttons (consider adding course info if needed later)
            st.button("Schedule Session", key=f"schedule_{group.get('groupid')}")
            st.button("Leave Group", key=f"leave_{group.get('groupid')}")
            st.divider()
    else:
        st.write("You haven't joined any groups yet.")
    # --- End of study groups section ---

with find_groups_tab:
    st.subheader("Find Existing Study Groups")
    
    # --- Fetch and display available groups from API ---
    available_groups, error = get_available_groups()
    
    if error:
        st.error(f"Could not load available groups: {error}")
    elif available_groups: # Check if the list is not empty
        # Simple search filter (filtering happens client-side for now)
        # Note: Course filtering won't work accurately without course info from API
        search_term = st.text_input("Search by group name")
        
        st.divider()
        st.write("**Available Groups**")
        
        # Filter groups based on search term
        if search_term:
            filtered_groups = [
                g for g in available_groups 
                if search_term.lower() in g.get('group_name', '').lower()
            ]
        else:
            filtered_groups = available_groups
            
        if filtered_groups:
            for group in filtered_groups:
                st.write(f"**{group.get('group_name', 'Unnamed Group')}**")
                # Add Description later if included in API/DB
                # st.write(f"Description: {group.get('description', 'N/A')}")
                group_id = group.get('groupid')
                join_button_key = f"join_{group_id}"
                if st.button("Request to Join", key=join_button_key):
                    user_id = st.session_state.user.get('id')
                    if group_id and user_id:
                        result, error = join_study_group(group_id, user_id)
                        if error:
                            st.error(f"Failed to join group: {error}")
                        else:
                            st.success(result.get("message", "Successfully processed join request!"))
                            # Optionally add st.rerun() here if immediate refresh of 'My Groups' is desired
                    else:
                        st.error("Cannot join group: Missing group or user ID.")
                    
                st.divider()
        else:
            st.write("No study groups found matching your search.")
    else:
        st.write("No study groups found.")
    # --- End of find groups section ---

with create_group_tab:
    st.subheader("Create a New Study Group")
    
    # Simple form for creating a group
    with st.form("create_group_form"):
        group_name = st.text_input("Group Name")
        # Course and Description are not sent to the backend for this simple create
        course = st.selectbox(
            "Related Course (Optional)", # Changed label slightly
            ["CS3200", "CS2500", "CS3000", "CS2510", "FINA2201", "CS4530", "MKTG2201", "ENGW1111", "MATH2332", ""], 
            index=None,
            placeholder="Select course..."
        )
        description = st.text_area("Description (Optional)") # Changed label slightly
        
        submitted = st.form_submit_button("Create Group")
        if submitted:
            # Basic validation for required field
            if group_name:
                user_id = st.session_state.user.get('id')
                # Call the API to create the group
                result, error = create_study_group(group_name, user_id)
                
                if error:
                    st.error(f"Failed to create group: {error}")
                elif result:
                    st.success(f"Group '{result.get('group', {}).get('group_name', group_name)}' created successfully!")
                    # Optionally clear the form or redirect, but for now just show success
            else:
                st.error("Please enter a Group Name.") 