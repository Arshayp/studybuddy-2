# naman
##################################################
# Main entry point for the StudyBuddy application.
# Handles routing based on login status.
##################################################

import streamlit as st
from modules.nav import setup_page # Import setup_page for theme/sidebar

# Set page config first
st.set_page_config(
    page_title="StudyBuddy Dashboard",
    page_icon="📚",
    layout="wide"
)

# Initialize session state if keys don't exist
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user" not in st.session_state:
    st.session_state.user = {}

# --- Page Logic ---
if not st.session_state.logged_in:
    # If not logged in, show login page
    st.switch_page("pages/login.py")
    st.stop()
else:
    # If logged in, setup sidebar and check login status again
    setup_page("Dashboard") 
    
    st.header("Welcome to your StudyBuddy Dashboard!")
    
    # Layout columns
    left_col, right_col = st.columns(2)
    
    with left_col:
        st.subheader("Your Study Groups")
        # Display study groups (example data)
        groups = [
            {"name": "CS3200 Study Group", "next_session": "Tomorrow at 3 PM"},
            {"name": "FINA2201 Study Group", "next_session": "Friday at 2 PM"}
        ]
        
        if groups:
            for group in groups:
                with st.expander(f"**{group['name']}**"):
                    st.write(f"Next Session: {group.get('next_session', 'Not scheduled')}")
                    st.button("Join Session", key=f"join_{group['name']}") # Button doesn't do anything yet
        else:
            st.write("You haven't joined any study groups yet.")
        
        st.subheader("Study Resources")
        # Display resources (example data)
        resources = [
            {"name": "Programming Basics PDF", "type": "Document"},
            {"name": "Math Formula Sheet", "type": "Document"}
        ]
        
        if resources:
            for resource in resources:
                with st.expander(f"**{resource['name']}**"):
                    st.write(f"Type: {resource.get('type', 'N/A')}")
                    st.button("Access", key=f"access_{resource['name']}") # Button doesn't do anything yet
        else:
            st.write("No study resources available yet.")
    
    with right_col:
        st.subheader("Profile Summary")
        # Show basic user info from session state
        user_info = st.session_state.user 
        st.write(f"Name: {user_info.get('name', 'N/A')}")
        st.write(f"University: {user_info.get('university', 'N/A')}")
        st.write(f"Major: {user_info.get('major', 'N/A')}")
        
        if st.button("Edit Profile", use_container_width=True):
            st.switch_page("pages/profile.py")
        
        st.subheader("Study Matches")
        # Display matches (example data)
        matches = [
            {"name": "Alex CHen", "compatibility": "95%"},
            {"name": "Emily Rodriguez", "compatibility": "88%"}
        ]
        
        if matches:
            for match in matches:
                st.write(f"**{match['name']}** - {match.get('compatibility', 'N/A')} Match")
                st.button("Connect", key=f"connect_{match['name']}") # Button doesn't do anything yet
        else:
            st.write("No recent matches found.")