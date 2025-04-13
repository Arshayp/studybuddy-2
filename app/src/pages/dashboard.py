# naman
import streamlit as st
from datetime import datetime
from modules.nav import setup_page

# Page Configuration
st.set_page_config(
    page_title="StudyBuddy - Dashboard",
    page_icon="📊",
    layout="wide"
)

# Setup: Theme, Auth, Sidebar
setup_page("Dashboard") 

# --- Page Content ---
st.title("StudyBuddy Dashboard")

left_col, right_col = st.columns(2)

with left_col:
    st.subheader("Your Study Groups")
    # Example data - replace with actual data later
    groups = [
        {"name": "CS101 Study Group", "next_session": "Tomorrow at 3 PM"},
        {"name": "Math Analysis Group", "next_session": "Friday at 2 PM"}
    ]
    
    if groups:
        for group in groups:
            with st.expander(f"**{group['name']}**"):
                st.write(f"Next Session: {group.get('next_session', 'N/A')}")
                st.button("Join Session", key=f"join_{group['name']}")
    else:
        st.write("You are not in any study groups.")
    
    st.subheader("Study Resources")
    # Example data
    resources = [
        {"name": "Programming Basics PDF", "type": "Document"},
        {"name": "Math Formula Sheet", "type": "Document"}
    ]
    
    if resources:
        for resource in resources:
            with st.expander(f"**{resource['name']}**"):
                st.write(f"Type: {resource.get('type', 'N/A')}")
                st.button("Access", key=f"access_{resource['name']}")
    else:
        st.write("No study resources found.")

with right_col:
    st.subheader("Profile Summary")
    user_info = st.session_state.get('user', {})
    st.write(f"Name: {user_info.get('name', 'N/A')}")
    st.write(f"Email: {user_info.get('email', 'N/A')}") # Display email too?
    
    if st.button("Edit Profile & Settings", use_container_width=True):
        st.switch_page("pages/profile.py")
    
    st.subheader("Study Matches")
    # Example data
    matches = [
        {"name": "Alex", "compatibility": "95%"},
        {"name": "Jordan", "compatibility": "88%"}
    ]
    
    if matches:
        for match in matches:
            st.write(f"**{match['name']}** - {match.get('compatibility', 'N/A')} Match")
            st.button("Connect", key=f"connect_{match['name']}")
    else:
        st.write("No recent matches found.") 