# naman
import streamlit as st
import requests # Import requests
from datetime import datetime # Keep for demo data?
from modules.nav import setup_page

API_BASE_URL="http://web-api:4000" # Define API Base URL

# Page Config
st.set_page_config(
    page_title="StudyBuddy - Find Partners",
    page_icon="🤝",
    layout="wide"
)

# Basic setup
setup_page("Find Partners")

# --- Helper function to fetch all users for matching ---
def get_all_users_for_matching():
    users_url = f"{API_BASE_URL}/u/match/all-matches" # Corrected endpoint path
    try:
        response = requests.get(users_url)
        if response.status_code == 200:
            # Extract list from the nested key
            data = response.json()
            user_list = data.get("students_or_users", [])
            return user_list, None # Return user list, no error
        else:
            return None, f"API Error: {response.status_code} - {response.text}"
    except requests.exceptions.RequestException as e:
        return None, f"Connection Error: {e}"
    except Exception as e:
        return None, f"Error processing user data: {str(e)}"

# --- Helper function to record a match ---
def record_match(user1_id, user2_id):
    if not user1_id or not user2_id:
        return None, "Missing user IDs for matching."
        
    match_url = f"{API_BASE_URL}/u/match/success"
    payload = {"user1_id": user1_id, "user2_id": user2_id}
    try:
        response = requests.post(match_url, json=payload)
        if response.status_code == 200:
            return response.json(), None # Return success message, no error
        else:
            error_detail = response.json().get("error", response.text) if response.content else response.reason
            return None, f"API Error ({response.status_code}): {error_detail}"
    except requests.exceptions.RequestException as e:
        return None, f"Connection Error: {e}"
    except Exception as e: 
        return None, f"An unexpected error occurred: {str(e)}"

# --- Helper function to fetch current user's matches ---
def get_my_matches(user_id):
    if not user_id:
        return None, "User ID not found in session."
        
    my_matches_url = f"{API_BASE_URL}/u/match/{user_id}/matches"
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

st.title("Find Study Partners")

# Tabs for different sections
find_tab, matches_tab, preferences_tab = st.tabs(["Find Partners", "My Matches", "Matching Preferences"])

with find_tab:
    st.subheader("Available Study Partners")
    
    # Removed Filters for now, as API returns all users
    # We can add client-side filtering later if needed
    
    # --- Fetch and display users from API ---
    all_users, error = get_all_users_for_matching()
    current_user_id = st.session_state.user.get('id') # Get logged-in user ID
    
    if error:
        st.error(f"Could not load potential partners: {error}")
    elif all_users:
        st.write("### Potential Study Partners")
        
        potential_partners = [user for user in all_users if user.get('userid') != current_user_id]

        if potential_partners:
            for partner in potential_partners:
                partner_id = partner.get('userid')
                # Display relevant info (excluding password!)
                st.write(f"**{partner.get('name', 'Unknown User')}**")
                st.write(f"Major: {partner.get('major', 'N/A')}")
                st.write(f"Learning Style: {partner.get('learning_style', 'N/A')}")
                st.write(f"Availability: {partner.get('availability', 'N/A')}")
                
                # --- Connect Button Logic --- 
                connect_key = f"connect_{partner_id}" # Unique key for each button
                if st.button("Connect", key=connect_key):
                    if current_user_id and partner_id:
                        # Call API to record the match
                        result, match_error = record_match(current_user_id, partner_id)
                        if match_error:
                            st.error(f"Could not connect with {partner.get('name')}: {match_error}")
                        else:
                            # Display success message from API
                            st.success(result.get("message", f"Connected with {partner.get('name')}!"))
                    else:
                         st.error("Could not initiate connection (missing user IDs).")
                # --- End Connect Button Logic ---
                
                st.divider()
        else:
             st.write("No other users found.") # Case where only the current user exists
            
    else:
        st.write("No potential partners found.")

with matches_tab:
    st.subheader("Your Current Matches") # Removed '& Requests' for now
    
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
            st.button("Unmatch", key=f"my_matches_unmatch_{matched_user_id}") # Placeholder
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