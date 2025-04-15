import streamlit as st
from modules.nav import setup_page
import plotly.express as px
import pandas as pd

# Page Configuration
st.set_page_config(
    page_title="StudyBuddy - Emily's Profile",
    page_icon="👤",
    layout="wide"
)

# Setup
setup_page("Emily's Profile")

# User Information
st.title("Emily Rodriguez's Academic Profile")

# Create tabs for different sections
goals_tab, courses_tab, metrics_tab, partners_tab = st.tabs([
    "Semester Goals", 
    "Course Targets", 
    "Study Metrics", 
    "Study Partners"
])

# Semester Goals Tab
with goals_tab:
    st.header("📚 Semester Goals")
    
    # Create columns for goals
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Academic Goals")
        goals = [
            "Maintain a 3.8+ GPA",
            "Complete all assignments on time",
            "Participate in 2 study groups per week",
            "Attend all professor office hours"
        ]
        for goal in goals:
            st.checkbox(goal, value=True)
    
    with col2:
        st.subheader("Personal Development")
        personal_goals = [
            "Improve time management skills",
            "Develop better note-taking techniques",
            "Balance study and social life",
            "Learn 2 new study techniques"
        ]
        for goal in personal_goals:
            st.checkbox(goal, value=True)

# Course Targets Tab
with courses_tab:
    st.header("📖 Course Progress")
    
    # Sample course data
    courses = {
        "Calculus II": 75,
        "Data Structures": 85,
        "Physics I": 60,
        "English Literature": 90
    }
    
    for course, progress in courses.items():
        st.subheader(course)
        st.progress(progress / 100)
        st.write(f"Current Progress: {progress}%")

# Study Metrics Tab
with metrics_tab:
    st.header("📊 Study Habits & Performance")
    
    # Create columns for metrics
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Weekly Study Hours")
        # Sample data for study hours
        data = {
            'Day': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            'Hours': [3, 4, 2, 5, 3, 2, 1]
        }
        df = pd.DataFrame(data)
        fig = px.bar(df, x='Day', y='Hours', title='Study Hours by Day')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Study Efficiency")
        efficiency_metrics = {
            "Focus Time": "85%",
            "Distractions": "2 per hour",
            "Retention Rate": "78%",
            "Study Sessions": "14 this week"
        }
        for metric, value in efficiency_metrics.items():
            st.metric(metric, value)

# Study Partners Tab
with partners_tab:
    st.header("👥 Study Partners")
    
    # Create columns for different types of study partners
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Study Groups")
        study_groups = [
            "Calculus Study Group (Mon, Wed 4-6pm)",
            "Data Structures Group (Tue, Thu 2-4pm)",
            "Physics Lab Partners"
        ]
        for group in study_groups:
            st.write(f"📚 {group}")
    
    with col2:
        st.subheader("One-on-One Partners")
        partners = [
            "Sarah Johnson (Calculus)",
            "Michael Chen (Data Structures)",
            "David Wilson (Physics)"
        ]
        for partner in partners:
            st.write(f"👤 {partner}")
            
    # Add a button to find new study partners
    if st.button("Find New Study Partners"):
        st.info("Feature coming soon! You'll be able to find new study partners based on your courses and availability.") 