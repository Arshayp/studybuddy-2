# naman
import streamlit as st
from datetime import datetime # Keep for demo data
from modules.nav import setup_page

# Page Config
st.set_page_config(
    page_title="StudyBuddy - Study Groups",
    page_icon="👥",
    layout="wide"
)

# Basic setup
setup_page("Study Groups")

st.title("Study Groups")

# Tabs for sections
my_groups_tab, find_groups_tab, create_group_tab = st.tabs(["My Groups", "Find Groups", "Create Group"])

with my_groups_tab:
    st.subheader("Your Study Groups")
    
    # Example data
    groups = [
        {"id": 1, "name": "CS3200 Databases Study Group", "course": "CS3200"},
        {"id": 2, "name": "Financial Management Study Group", "course": "FINA2201"}
    ]
    
    if groups:
        for group in groups:
            st.write(f"**{group.get('name', 'Unnamed Group')}** ({group.get('course', 'N/A')})")
            # Simple action buttons
            st.button("Schedule Session", key=f"schedule_{group['id']}")
            st.button("Leave Group", key=f"leave_{group['id']}")
            st.divider()
    else:
        st.write("You haven't joined any groups yet.")

with find_groups_tab:
    st.subheader("Find Existing Study Groups")
    
    # Simple search filter
    course_filter = st.selectbox(
        "Filter by Course",
        ["All Courses", "CS101", "CS201", "MATH101", "MATH201"], 
    )
    
    st.divider()
    st.write("**Available Groups**")
    # Example data
    available_groups = [
        {"id": 3, "name": "Algorithms Study Group", "course": "CS3000", "description": "Practice algorithms"},
        {"id": 4, "name": "Fundies Study Group", "course": "CS2510", "description": "Solve problems"}
    ]
    
    # Basic filtering display
    filtered_groups = available_groups
    if course_filter != "All Courses":
        filtered_groups = [g for g in filtered_groups if g.get('course') == course_filter]
    
    if filtered_groups:
        for group in filtered_groups:
            st.write(f"**{group.get('name', 'Unnamed Group')}** ({group.get('course', 'N/A')})")
            st.write(f"Description: {group.get('description', 'N/A')}")
            st.button("Request to Join", key=f"join_{group['id']}")
            st.divider()
    else:
        st.write("No study groups found for this course.")

with create_group_tab:
    st.subheader("Create a New Study Group")
    
    # Simple form for creating a group
    with st.form("create_group_form"):
        group_name = st.text_input("Group Name")
        course = st.selectbox(
            "Course",
            ["CS3200", "CS2500", "CS3000", "CS2510", "FINA2201", "CS4530", "MKTG2201", "ENGW1111", "MATH2332", ""], 
            index=None,
            placeholder="Select course..."
        )
        description = st.text_area("Description")
        
        submitted = st.form_submit_button("Create Group")
        if submitted:
            # Basic validation
            if group_name and course:
                # Placeholder action
                st.success(f"Group '{group_name}' created! (Demo)")
            else:
                st.error("Please enter a Group Name and select a Course.") 