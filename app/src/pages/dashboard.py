# naman
import streamlit as st
import requests # Import requests
from datetime import datetime
from modules.nav import setup_page

API_BASE_URL="http://web-api:4000/"

# Page Configuration
st.set_page_config(
    page_title="StudyBuddy - Dashboard",
    page_icon="📊",
    layout="wide"
)

# Setup: Theme, Auth, Sidebar
setup_page("Dashboard") 

# --- Helper function to fetch resources ---
def get_user_resources(user_id):
    if not user_id:
        return None, "User ID not found in session."
    
    resources_url = f"{API_BASE_URL}/u/{user_id}/resources"
    try:
        response = requests.get(resources_url)
        if response.status_code == 200:
            return response.json(), None # Return data, no error
        else:
            return None, f"API Error: {response.status_code} - {response.text}"
    except requests.exceptions.RequestException as e:
        return None, f"Connection Error: {e}"

# --- Helper function to fetch potential matches ---
def get_potential_matches(user_id):
    if not user_id:
        return None, "User ID not found in session."
        
    matches_url = f"{API_BASE_URL}/u/potential-matches"
    payload = {"user_id": user_id}
    try:
        response = requests.post(matches_url, json=payload)
        if response.status_code == 200:
            return response.json(), None # Return data, no error
        else:
            return None, f"API Error: {response.status_code} - {response.text}"
    except requests.exceptions.RequestException as e:
        return None, f"Connection Error: {e}"

# --- Helper function to fetch user's study groups ---
def get_user_study_groups(user_id):
    if not user_id:
        return None, "User ID not found in session."
        
    groups_url = f"{API_BASE_URL}/u/groups/all"
    payload = {"user_id": user_id}
    try:
        response = requests.post(groups_url, json=payload)
        if response.status_code == 200:
            return response.json(), None # Return data, no error
        else:
            return None, f"API Error: {response.status_code} - {response.text}"
    except requests.exceptions.RequestException as e:
        return None, f"Connection Error: {e}"

# --- Page Content ---
st.title("StudyBuddy Dashboard")

left_col, right_col = st.columns(2)

with left_col:
    st.subheader("Your Study Groups")
    # --- Fetch and display user's study groups from API ---
    user_id = st.session_state.user.get('id')
    groups, error = get_user_study_groups(user_id)

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