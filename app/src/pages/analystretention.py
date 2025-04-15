import streamlit as st
import plotly.express as px
import pandas as pd
from modules.nav import setup_page

# Page Configuration
st.set_page_config(
    page_title="Retention Analysis",
    page_icon="📈",
    layout="wide"
)

# Set current page in session state
st.session_state.page = 'analystretention'

# Setup page
setup_page("Retention Analysis")

# Sidebar navigation
st.sidebar.title("Analytics Navigation")

if st.sidebar.button("Dashboard", use_container_width=True, key="nav_dashboard_ret"):
    st.switch_page("pages/dataanalystdashboard.py")
    
if st.sidebar.button("Student Matching", use_container_width=True, key="nav_matching_ret"):
    st.switch_page("pages/analyststudentmatching.py")
    
if st.sidebar.button("Retention Analysis", use_container_width=True, key="nav_retention_ret"):
    st.switch_page("pages/analystretention.py")
    
if st.sidebar.button("Geographic Data", use_container_width=True, key="nav_geographic_ret"):
    st.switch_page("pages/analystgeographic.py")
    
if st.sidebar.button("Academic Insights", use_container_width=True, key="nav_academic_ret"):
    st.switch_page("pages/analystacademic.py")

st.sidebar.divider()

# Main content
st.title("Retention Analysis")
st.write("Explore student retention trends and key metrics.")

# Top metrics row
col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Current Retention Rate",
        "86%",
        "+3% vs last month"
    )

with col2:
    st.metric(
        "At-Risk Students",
        "142",
        "-8% vs last month"
    )

# Simple retention over time chart
st.subheader("Retention Over Time")
retention_data = pd.DataFrame({
    'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
    'Retention': [90, 88, 85, 86, 86]
})
fig = px.line(
    retention_data,
    x='Month',
    y='Retention',
    markers=True
)
fig.update_traces(line_color='#1a1a2e')
st.plotly_chart(fig, use_container_width=True)

# Add a second simple graph: Retention by Cohort
st.subheader("Retention by Cohort")
cohort_data = pd.DataFrame({
    'Cohort': ['Fall 2023', 'Spring 2024', 'Summer 2024'],
    'Retention': [88, 91, 85]
})
fig2 = px.bar(
    cohort_data,
    x='Cohort',
    y='Retention',
    text='Retention',
    color='Cohort',
    color_discrete_sequence=['#1a1a2e', '#4a4a5a', '#8a8a9a']
)
fig2.update_traces(texttemplate='%{text}%', textposition='outside')
fig2.update_layout(showlegend=False, yaxis_range=[0, 100])
st.plotly_chart(fig2, use_container_width=True) 