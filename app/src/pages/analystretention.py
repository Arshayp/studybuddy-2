import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from modules.nav import setup_page

API_BASE_URL = "http://web-api:4000"

# Page Config
st.set_page_config(
    page_title="Retention Analytics",
    page_icon="📊",
    layout="wide"
)

# Set current page in session state
st.session_state.page = 'analystretention'

# Basic setup
setup_page("Retention Analytics")

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
st.title("Retention Analytics")
st.write("Track and analyze student retention patterns and study group dynamics.")

# Helper function to fetch analytics data
def get_cohort_analytics():
    try:
        response = requests.get(f"{API_BASE_URL}/study/cohort-analytics")
        if response.status_code == 200:
            return response.json()
        return None
    except Exception:
        return None

# Fetch data silently (without showing errors)
analytics_data = get_cohort_analytics()

# Top metrics row
col1, col2, col3 = st.columns(3)

with col1:
    retention_rate = "86%"
    retention_change = "+3% vs last term"
    if analytics_data and 'retention_rate' in analytics_data:
        retention_rate = f"{analytics_data['retention_rate']}%"
        retention_change = analytics_data.get('retention_change', 'No change')
    
    st.metric(
        "Overall Retention Rate",
        retention_rate,
        retention_change
    )

with col2:
    active_groups = "2,047"
    groups_change = "+12% vs last month"
    if analytics_data and 'groups' in analytics_data:
        active_groups = str(len(analytics_data['groups']))
        groups_change = analytics_data.get('groups_change', 'No change')
    
    st.metric(
        "Active Study Groups",
        active_groups,
        groups_change
    )

with col3:
    avg_size = "4.8"
    size_change = "+0.3 vs last month"
    if analytics_data and 'avg_group_size' in analytics_data:
        avg_size = str(analytics_data['avg_group_size'])
        size_change = analytics_data.get('size_change', 'No change')
    
    st.metric(
        "Avg Group Size",
        avg_size,
        size_change
    )

# Study Group Activity Chart
st.subheader("Study Group Activity Trends")

if analytics_data and 'activity_trends' in analytics_data:
    activity_data = pd.DataFrame(analytics_data['activity_trends'])
else:
    # Demo data if API data is not available
    activity_data = pd.DataFrame({
        'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
        'Active Groups': [1800, 1900, 1950, 2000, 2047],
        'New Members': [200, 180, 220, 190, 210]
    })

fig = px.line(
    activity_data,
    x='Month',
    y=['Active Groups', 'New Members'],
    markers=True
)
fig.update_layout(yaxis_title="Count", xaxis_title="")
st.plotly_chart(fig, use_container_width=True)

# Retention by Major
st.subheader("Retention Rate by Major")

if analytics_data and 'major_retention' in analytics_data:
    major_data = pd.DataFrame(analytics_data['major_retention'])
else:
    # Demo data if API data is not available
    major_data = pd.DataFrame({
        'Major': ['Computer Science', 'Engineering', 'Biology', 'Business'],
        'Retention Rate': [92, 88, 85, 83]
    })

fig2 = px.bar(
    major_data,
    x='Major',
    y='Retention Rate',
    text='Retention Rate',
    color='Major',
    color_discrete_sequence=['#1a1a2e', '#4a4a5a', '#8a8a9a', '#cccccc']
)
fig2.update_traces(texttemplate='%{text}%', textposition='outside')
fig2.update_layout(showlegend=False, yaxis_range=[0, 100])
st.plotly_chart(fig2, use_container_width=True)

# Create two columns for the dashboard
col1, col2 = st.columns(2)
    
with col1:
    st.subheader("Study Groups Overview")
    if analytics_data and 'groups' in analytics_data:
        groups = analytics_data['groups']
        if groups:
            # Convert to DataFrame for better visualization
            df_groups = pd.DataFrame(groups)
            
            # Display groups in a nice table
            st.dataframe(
                df_groups.rename(columns={
                    'Group_ID': 'ID',
                    'Leader_Name': 'Group Leader',
                    'Leader_Major': 'Major'
                }),
                hide_index=True
            )
            
            # Show total groups metric
            st.metric("Total Study Groups", len(groups))
        else:
            st.info("No study groups available")
    
with col2:
    st.subheader("Study Session Analytics")
    if analytics_data and 'sessions' in analytics_data:
        sessions = analytics_data['sessions']
        if sessions:
            # Convert to DataFrame
            df_sessions = pd.DataFrame(sessions)
            
            # Create a bar chart of sessions per course
            st.bar_chart(
                df_sessions.set_index('Course_Name')['session_count'],
                use_container_width=True
            )
            
            # Show total sessions and active students metrics
            total_sessions = df_sessions['session_count'].sum()
            total_active = df_sessions['active_students'].sum()
            
            metrics_col1, metrics_col2 = st.columns(2)
            with metrics_col1:
                st.metric("Total Sessions", total_sessions)
            with metrics_col2:
                st.metric("Active Students", total_active)
        else:
            st.info("No session data available")