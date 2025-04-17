# naman
import streamlit as st
import requests # Import requests
from datetime import datetime # Keep for demo data?
from modules.nav import setup_page

# API_BASE_URL = "http://127.0.0.1:5000" # Adjust if backend runs elsewhere
API_BASE_URL = "http://web-api:4000" # Use Docker service name

# Page Config
st.set_page_config(
    page_title="StudyBuddy - Find Partners",
    page_icon="🤝",
    layout="wide"
)

# Basic setup
setup_page("Find Partners")




def get_all_users_for_display():
    """Fetches all users for display in the Find Partners tab."""
    all_users_url = f"{API_BASE_URL}/users/all" # Use the new endpoint
    try:
        response = requests.get(all_users_url)
        response.raise_for_status()
        return response.json(), None
    except requests.exceptions.RequestException as e:
        return None, str(e)
    except Exception as e:
        return None, f"An unexpected error occurred: {str(e)}"

# --- Helper function to record a successful match (POST request) ---
def record_match(user1_id, user2_id):
    """Records a match between two users using the new POST /matches endpoint."""
    if not user1_id or not user2_id:
        return None, "Missing user IDs for matching."

    match_url = f"{API_BASE_URL}/matches" # Use the new endpoint
    payload = {"user1_id": user1_id, "user2_id": user2_id}
    try:
        response = requests.post(match_url, json=payload)
        response.raise_for_status() # Check for 2xx status codes
        return response.json(), None
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
    # Removed previous TODO and return statement

# --- Helper function to fetch confirmed matches for a user (GET request) ---
def get_my_matches(user_id):
    if not user_id:
        return None, "User ID not provided."
    # my_matches_url = f"{API_BASE_URL}/u/match/{user_id}/matches"
    my_matches_url = f"{API_BASE_URL}/users/{user_id}/matches" # Updated URL
    try:
        response = requests.get(my_matches_url)
        if response.status_code == 200:
            return response.json(), None # Return list of matched users, no error
        else:
            error_detail = response.json().get("error", response.text) if response.content else response.reason
            return None, f"API Error ({response.status_code}): {error_detail}"
    except requests.exceptions.RequestException as e:
        return None, f"Connection Error: {e}"
    except Exception as e: 
        return None, f"An unexpected error occurred: {str(e)}"

# --- Helper function to delete a match (DELETE request) ---
def delete_match(user1_id, user2_id):
    """Deletes a match between two users."""
    if not user1_id or not user2_id:
        return None, "Missing user IDs for deletion."

    # Ensure consistent order for the URL
    # Although the backend should handle order, doing it client-side is also fine
    u1 = min(user1_id, user2_id)
    u2 = max(user1_id, user2_id)
    
    delete_url = f"{API_BASE_URL}/matches/{u1}/{u2}"
    try:
        response = requests.delete(delete_url)
        response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
        return response.json(), None # Return success message
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

st.title("Find Study Partners")

# Tabs for different sections
find_tab, matches_tab, preferences_tab = st.tabs(["Find Partners", "My Matches", "Matching Preferences"])

with find_tab:
    st.subheader("Available Study Partners")
    
    # Removed Filters for now, as API returns all users
    # We can add client-side filtering later if needed
    
    # --- Fetch and display users from API ---
    current_user_id = st.session_state.user.get('id') 
    # potential_partners, error = get_potential_matches(current_user_id)
    all_partners_list, error = get_all_users_for_display()
    
    if error:
        st.error(f"Could not load potential partners: {error}")
    # elif potential_partners:
    elif all_partners_list is not None: # Check if fetch was successful (even if list is empty)
        st.write("#### Available Study Partners :-) ")
        if not all_partners_list:
            st.write("No users found.")
        else:
            # Display all users fetched
            for partner in all_partners_list:
                partner_id = partner.get('userid')
                # Display relevant info
                st.write(f"**{partner.get('name', 'Unknown User')}**") # fallback in case that the partner does not have a name; troubleshooting but this doesnt happen anymore :)
                st.write(f"Major: {partner.get('major', 'N/A')}")
                st.write(f"Learning Style: {partner.get('learning_style', 'N/A')}")
                st.write(f"Availability: {partner.get('availability', 'N/A')}")
                
                # --- Connect Button Logic --- 
                connect_key = f"connect_{partner_id}" 
                # Disable button if it's the current user
                disable_button = (partner_id == current_user_id)
                if st.button("Connect", key=connect_key, disabled=disable_button):
                    if current_user_id and partner_id:
                        # Call API to record the match
                        result, match_error = record_match(current_user_id, partner_id)
                        if match_error:
                            st.error(f"Could not connect with {partner.get('name')}: {match_error}")
                        else:
                            # Display success/info message from API
                            # Check status code or message content if needed for different messages
                            st.success(result.get("message", f"Connection action processed for {partner.get('name')}!")) 
                            # No st.rerun() needed as per user feedback
                    else:
                         st.error("Could not initiate connection (missing user IDs).")
                # --- End Connect Button Logic --- 
                
                st.divider()
            
    else: # Error case handled above, this handles case where API returns None unexpectedly
        st.error("An unexpected issue occurred while loading users.")

with matches_tab:
    st.subheader("Your Current Matches")
    
    # --- Fetch and display current matches from API ---
    current_user_id = st.session_state.user.get('id')
    my_matches_list, error = get_my_matches(current_user_id)
    
    if error:
        st.error(f"Could not load your matches: {error}")
    elif my_matches_list:
        st.write("Here are the users you are matched with:")
        for match in my_matches_list:
            # API returns matched_user_name and matched_user_id
            matched_user_id = match.get('matched_user_id') # Get the ID once
            st.write(f"**{match.get('matched_user_name', 'Unknown User')}**")
            
            # Simple buttons 
            # Add Course/Status later if needed and available from API/DB
            # Add a tab-specific prefix to the keys
            st.button("Message", key=f"my_matches_msg_{matched_user_id}")
            unmatch_button_key = f"my_matches_unmatch_{matched_user_id}"
            if st.button("Unmatch", key=unmatch_button_key):
                if current_user_id and matched_user_id:
                    result, error = delete_match(current_user_id, matched_user_id)
                    if error:
                        st.error(f"Failed to unmatch: {error}")
                    else:
                        st.success(result.get("message", "Successfully unmatched!"))
                        st.rerun() # Rerun to refresh the match list
                else:
                    st.error("Could not unmatch: Missing user IDs.")

            st.divider()
            
    else:
        st.write("You haven't matched with anyone yet.")
    # --- End of my matches section ---

with preferences_tab:
    st.subheader("Update Your Matching Preferences")
    
    # Simple form for preferences
    with st.form("matching_preferences"):
        st.write("Set your preferences to find better matches.")
        
        # Fewer options for simplicity
        preferred_styles = st.multiselect(
            "Preferred Learning Styles",
            ["Visual", "Auditory", "Reading/Writing", "Kinesthetic"],
            default=st.session_state.get('preferences', {}).get('preferred_styles', [])
        )
        availability_days = st.multiselect(
            "Available Days",
            ["Weekdays", "Weekends", "Any"],
            default=st.session_state.get('preferences', {}).get('availability_days', [])
        )
        goals = st.multiselect(
            "Study Goals",
            ["Improve Grades", "Homework Help", "Exam Prep"],
            default=st.session_state.get('preferences', {}).get('goals', [])
        )
                
        if st.form_submit_button("Save Preferences"):
            # Save preferences to session state (replace with backend later)
            st.session_state['preferences'] = {
                'preferred_styles': preferred_styles,
                'availability_days': availability_days,
                'goals': goals,
            }
            st.success("Preferences updated!") 