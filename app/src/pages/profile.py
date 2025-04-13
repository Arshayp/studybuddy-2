# naman
import streamlit as st
from modules.nav import setup_page

# Page Configuration
st.set_page_config(
    page_title="StudyBuddy - Profile",
    page_icon="👤",
    layout="wide"
)

# Setup
setup_page("Profile")

st.title("Your Profile & Settings")

# Use tabs for organization
info_tab, prefs_tab, account_tab = st.tabs(["Basic Info", "Study Preferences", "Account"])

with info_tab:
    st.subheader("Personal Information")
    
    # Simple form for info
    with st.form("info_form"):
        user_data = st.session_state.get('user', {})
        
        name = st.text_input("Name", value=user_data.get('name', ''))
        email = st.text_input("Email", value=user_data.get('email', ''), disabled=True) # Keep email read-only
        university = st.text_input("University", value=user_data.get('university', ''))
        major = st.text_input("Major", value=user_data.get('major', ''))
                
        if st.form_submit_button("Save Info"):
            # Update session state (replace with backend later)
            st.session_state['user'].update({
                'name': name,
                'university': university,
                'major': major,
            })
            st.success("Basic info updated!")

with prefs_tab:
    st.subheader("Study Preferences")
    
    with st.form("prefs_form"):
        pref_data = st.session_state.get('preferences', {})
        
        # Simplified options
        learning_style = st.selectbox(
            "Learning Style",
            ["Visual", "Auditory", "Reading/Writing", "Kinesthetic", "Not Specified"],
            index=0 # Default to Visual if not set
        )
        availability = st.multiselect(
            "Preferred Study Times",
            ["Weekdays", "Weekends", "Evenings"],
            default=pref_data.get('availability', [])
        )
        interests = st.text_input(
            "Academic Interests (comma-separated)", 
            value=", ".join(pref_data.get('interests', [])),
            placeholder="e.g., Programming, Calculus"
        )
        
        if st.form_submit_button("Save Preferences"):
            # Update session state (replace with backend later)
            # Basic parsing for text input interests
            interest_list = [i.strip() for i in interests.split(',') if i.strip()]
            st.session_state['preferences'] = {
                'learning_style': learning_style,
                'availability': availability,
                'interests': interest_list
            }
            st.success("Study preferences updated!")
            
with account_tab:
    st.subheader("Account Settings")
    
    # Simple settings - maybe combine password into its own form/page later
    settings_data = st.session_state.get('settings', {})
    
    notifications = st.checkbox("Enable Email Notifications", value=settings_data.get('notifications', True))
    
    st.divider()
    st.subheader("Change Password")
    with st.form("password_form"):
        current_password = st.text_input("Current Password", type="password")
        new_password = st.text_input("New Password", type="password")
        confirm_password = st.text_input("Confirm New Password", type="password")
        
        if st.form_submit_button("Change Password"):
             if not current_password:
                 st.error("Please enter your current password.")
             elif not new_password:
                 st.error("Please enter a new password.")
             elif new_password != confirm_password:
                 st.error("New passwords do not match.")
             else:
                 # Placeholder for backend password change call
                 st.success("Password changed successfully! (Demo)")
    
    # Button to save non-password settings
    if st.button("Save Notification Setting"):
         st.session_state['settings'] = {
             **(st.session_state.get('settings', {})), # Keep other settings
             'notifications': notifications
         }
         st.success("Notification setting saved!") 