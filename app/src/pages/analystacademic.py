import streamlit as st
import plotly.express as px
import pandas as pd
from modules.nav import setup_page

# Page Configuration
st.set_page_config(
    page_title="Academic Insights",
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
st.write("Explore academic performance trends and insights across courses and cohorts.")

# Top metrics row
col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Avg. GPA",
        "3.42",
        "+0.08 vs last term"
    )

with col2:
    st.metric(
        "Courses Above 90% Pass Rate",
        "12",
        "+2 vs last term"
    )

# Simple bar chart: Top Performing Courses
st.subheader("Top Performing Courses")
courses = pd.DataFrame({
    'Course': ['Calculus', 'Biology', 'Physics', 'Chemistry'],
    'Avg Grade': [91, 89, 87, 85]
})
fig = px.bar(
    courses,
    x='Course',
    y='Avg Grade',
    text='Avg Grade',
    color='Course',
    color_discrete_sequence=['#1a1a2e', '#4a4a5a', '#8a8a9a', '#cccccc']
)
fig.update_traces(texttemplate='%{text}', textposition='outside')
fig.update_layout(showlegend=False, yaxis_range=[0, 100])
st.plotly_chart(fig, use_container_width=True)

# Simple pie chart: Grade Distribution
st.subheader("Grade Distribution")
grade_dist = pd.DataFrame({
    'Grade': ['A', 'B', 'C', 'D', 'F'],
    'Count': [120, 95, 60, 15, 5]
})
fig2 = px.pie(
    grade_dist,
    names='Grade',
    values='Count',
    color_discrete_sequence=['#1a1a2e', '#4a4a5a', '#8a8a9a', '#cccccc', '#e0e0e0']
)
fig2.update_traces(textinfo='percent+label')
st.plotly_chart(fig2, use_container_width=True) 