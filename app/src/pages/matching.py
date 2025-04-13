# naman
import streamlit as st
from datetime import datetime # Keep for demo data
from modules.nav import setup_page

# Page Config
st.set_page_config(
    page_title="StudyBuddy - Find Partners",
    page_icon="🤝",
    layout="wide"
)

# Basic setup
setup_page("Find Partners")

st.title("Find Study Partners")

# Tabs for different sections
find_tab, matches_tab, preferences_tab = st.tabs(["Find Partners", "My Matches", "Matching Preferences"])

with find_tab:
    st.subheader("Search for Study Partners")
    
    # Simple filters
    course = st.selectbox(
        "Course",
        ["All Courses", "CS101", "CS201", "MATH101", "MATH201"], 
    )
    learning_style = st.multiselect(
        "Learning Style",
        ["Visual", "Auditory", "Reading/Writing", "Kinesthetic"],
    )
    
    if st.button("Find Matches"):
        st.write("### Potential Study Partners")
        
        # Example data
        matches_data = [
            {"id": 1, "name": "Alex", "course": "CS101", "compatibility": 95},
            {"id": 2, "name": "Jordan", "course": "MATH201", "compatibility": 88},
            {"id": 5, "name": "Chris", "course": "CS101", "compatibility": 85}
        ]
        
        # Simple display
        if matches_data:
            for match in matches_data:
                st.write(f"**{match['name']}** ({match.get('course', 'N/A')}) - {match.get('compatibility', 'N/A')}% Match")
                col1, col2 = st.columns(2)
                with col1:
                    st.button("Connect", key=f"connect_{match['id']}")
                with col2:
                    st.button("View Profile", key=f"profile_{match['id']}")
                st.divider()
        else:
            st.write("No matches found.")

with matches_tab:
    st.subheader("Your Current Matches & Requests")
    
    # Example data
    current_matches_data = [
        {"id": 3, "name": "Taylor", "course": "CS101", "status": "Connected"},
        {"id": 4, "name": "Sam", "course": "MATH201", "status": "Pending"}
    ]
    
    if current_matches_data:
        for match in current_matches_data:
            status = match.get('status', 'Unknown')
            st.write(f"**{match['name']}** ({match.get('course', 'N/A')}) - Status: {status}")
            
            # Simple buttons based on status
            if status == "Connected":
                st.button("Message", key=f"msg_{match['id']}")
            elif status == "Pending": 
                st.button("Accept Request", key=f"accept_{match['id']}")
                st.button("Decline Request", key=f"decline_{match['id']}")
            st.divider()
            
    else:
        st.write("You don't have any matches or requests yet.")

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