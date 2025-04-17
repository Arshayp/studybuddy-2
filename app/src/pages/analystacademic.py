import streamlit as st
import plotly.express as px
import pandas as pd
import requests
from modules.nav import setup_page

API_BASE_URL = "http://web-api:4000"

# Page Configuration
st.set_page_config(
    page_title="StudyBuddy - Academic Insights",
    page_icon="🎓",
    layout="wide"
)

# Set current page in session state
st.session_state.page = 'analystacademic'

# Setup page
setup_page("Academic Insights")

# Sidebar navigation
st.sidebar.title("Analytics Navigation")

if st.sidebar.button("Dashboard", use_container_width=True, key="nav_dashboard_acad"):
    st.switch_page("pages/dataanalystdashboard.py")
    
if st.sidebar.button("Student Matching", use_container_width=True, key="nav_matching_acad"):
    st.switch_page("pages/analyststudentmatching.py")
    
if st.sidebar.button("Retention Analysis", use_container_width=True, key="nav_retention_acad"):
    st.switch_page("pages/analystretention.py")
    
if st.sidebar.button("Geographic Data", use_container_width=True, key="nav_geographic_acad"):
    st.switch_page("pages/analystgeographic.py")
    
if st.sidebar.button("Academic Insights", use_container_width=True, key="nav_academic_acad"):
    st.switch_page("pages/analystacademic.py")

st.sidebar.divider()

# Main content
st.title("Academic Insights")
st.write("Explore academic performance trends and learning outcomes across courses.")

# Helper function to fetch analytics data
def get_academic_analytics():
    try:
        response = requests.get(f"{API_BASE_URL}/study/academic-analytics")
        if response.status_code == 200:
            return response.json()
        return None
    except Exception:
        return None

# Fetch data
analytics_data = get_academic_analytics()

# Top metrics row
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Average GPA",
        "3.42",
        "+0.08 vs last term"
    )

with col2:
    st.metric(
        "Pass Rate",
        "92%",
        "+2% vs last term"
    )

with col3:
    st.metric(
        "Study Hours/Week",
        "15.5",
        "+1.2 hours"
    )

with col4:
    st.metric(
        "Active Courses",
        "24",
        "+3 this term"
    )

# Create two columns for the first row of charts
left_col, right_col = st.columns(2)

with left_col:
    st.subheader("Top Performing Courses")
    
    # Course performance data
    course_data = pd.DataFrame({
        'Course': ['Calculus II', 'Physics 101', 'Chemistry', 'Biology'],
        'Average Grade': [92, 88, 85, 83]
    })
    
    fig = px.bar(
        course_data,
        x='Course',
        y='Average Grade',
        text=[f"{v}%" for v in course_data['Average Grade']],
        color='Course',
        color_discrete_sequence=['#1a1a2e', '#4a4a5a', '#8a8a9a', '#cccccc']
    )
    fig.update_traces(textposition='outside')
    fig.update_layout(
        showlegend=False,
        xaxis_title="",
        yaxis_title="Average Grade",
        yaxis_range=[0, 100]
    )
    st.plotly_chart(fig, use_container_width=True)

with right_col:
    st.subheader("Grade Distribution")
    
    # Grade distribution data
    grade_data = pd.DataFrame({
        'Grade': ['A', 'B', 'C', 'D', 'F'],
        'Students': [45, 30, 15, 7, 3]
    })
    
    fig = px.pie(
        grade_data,
        names='Grade',
        values='Students',
        color_discrete_sequence=['#1a1a2e', '#4a4a5a', '#8a8a9a', '#cccccc', '#e0e0e0']
    )
    fig.update_traces(textinfo='percent+label')
    st.plotly_chart(fig, use_container_width=True)

# Create two columns for the second row
left_col2, right_col2 = st.columns(2)

with left_col2:
    st.subheader("Study Time vs. Performance")
    
    # Study time vs performance data
    study_data = pd.DataFrame({
        'Hours': [5, 10, 15, 20, 25],
        'Average Grade': [75, 82, 88, 92, 95]
    })
    
    fig = px.scatter(
        study_data,
        x='Hours',
        y='Average Grade',
        labels={'Hours': 'Weekly Study Hours', 'Average Grade': 'Average Grade (%)'}
    )
    fig.update_traces(marker=dict(color='#1a1a2e', size=10))
    fig.update_layout(
        xaxis_title="Weekly Study Hours",
        yaxis_title="Average Grade (%)",
        yaxis_range=[70, 100]
    )
    st.plotly_chart(fig, use_container_width=True)

with right_col2:
    st.subheader("Learning Progress Over Time")
    
    # Learning progress data
    progress_data = pd.DataFrame({
        'Week': list(range(1, 11)),
        'Average Score': [70, 75, 78, 82, 85, 87, 88, 90, 91, 92]
    })
    
    fig = px.line(
        progress_data,
        x='Week',
        y='Average Score',
        markers=True,
        labels={'Week': 'Week Number', 'Average Score': 'Average Score (%)'}
    )
    fig.update_traces(line_color='#1a1a2e')
    st.plotly_chart(fig, use_container_width=True)

# Additional insights section
st.subheader("Key Academic Insights")

# Create three columns for insights
insight_col1, insight_col2, insight_col3 = st.columns(3)

with insight_col1:
    st.info("📚 Most Improved Subject: **Physics 101** with +5.2% increase in average grade")

with insight_col2:
    st.warning("⚠️ Challenging Area: **Organic Chemistry** with 68% pass rate")

with insight_col3:
    st.success("🎯 Best Study Pattern: **2-hour sessions** with 94% retention rate") 