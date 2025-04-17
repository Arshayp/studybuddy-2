import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
import requests
from modules.nav import setup_page
import plotly.graph_objects as go

# Page Configuration
st.set_page_config(
    page_title="StudyBuddy Analytics",
    page_icon="📊",
    layout="wide"
)

# Set current page in session state
st.session_state.page = 'dataanalystdashboard'

# Setup page
setup_page("Data Analysis Dashboard")

# Title and welcome message
st.title("StudyBuddy Analytics")

# Navigation in sidebar (using standard Streamlit components)
st.sidebar.title("Analytics Navigation")

if st.sidebar.button("← Back to Main Dashboard", use_container_width=True, key="nav_main"):
    st.switch_page("pages/dashboard.py")

st.sidebar.divider()

if st.sidebar.button("Dashboard", use_container_width=True, key="nav_dashboard"):
    st.switch_page("pages/dataanalystdashboard.py")
    
if st.sidebar.button("Student Matching", use_container_width=True, key="nav_matching"):
    st.switch_page("pages/analyststudentmatching.py")
    
if st.sidebar.button("Retention Analysis", use_container_width=True, key="nav_retention"):
    st.switch_page("pages/analystretention.py")
    
if st.sidebar.button("Academic Insights", use_container_width=True, key="nav_academic"):
    st.switch_page("pages/analystacademic.py")

st.sidebar.divider()

# Main content
st.write("Welcome back, Sophia! Here's your analytics summary.")

# Initialize session state for retention if not exists
if 'retention_rate' not in st.session_state:
    st.session_state.retention_rate = 0
    st.session_state.retention_change = "Loading..."

# Initialize session state for active groups if not exists
if 'active_groups' not in st.session_state:
    st.session_state.active_groups = 0
    st.session_state.active_groups_change = "0%"

# Top metrics row
col1, col2 = st.columns(2)

with col1:
    # Show loading spinner while fetching data
    with st.spinner('Fetching active groups data...'):
        try:
            response = requests.get('http://web-api:4000/a/analytics/study-groups/active', timeout=2)
            if response.status_code == 200:
                data = response.json()
                if data['status'] == 'success' and 'metrics' in data:
                    metrics = data['metrics']
                    st.session_state.active_groups = metrics['active_groups']
                    change_pct = metrics['change_percentage']
                    st.session_state.active_groups_change = f"{'+' if change_pct > 0 else ''}{change_pct}% vs last month"
            else:
                st.session_state.active_groups = 0
                st.session_state.active_groups_change = "Error fetching data"
        except requests.exceptions.RequestException:
            st.session_state.active_groups = 0
            st.session_state.active_groups_change = "API unavailable"
    
    st.metric(
        "Active Study Groups",
        f"{st.session_state.active_groups:,}",
        st.session_state.active_groups_change
    )

with col2:
    # Show loading spinner while fetching data
    with st.spinner('Fetching retention data...'):
        try:
            response = requests.get('http://web-api:4000/a/analytics/retention', timeout=2)
            if response.status_code == 200:
                data = response.json()
                st.session_state.retention_rate = data.get('retention_rate', 0)
                st.session_state.retention_change = data.get('retention_change', 0)
            else:
                st.session_state.retention_rate = 0
                st.session_state.retention_change = "Error fetching data"
        except requests.exceptions.RequestException:
            st.session_state.retention_rate = 0
            st.session_state.retention_change = "API unavailable"
    
    st.metric(
        "Retention Rate",
        f"{st.session_state.retention_rate}%",
        st.session_state.retention_change
    )

# Create two columns for the charts
col1, col2 = st.columns(2)

with col1:
    st.subheader("Student Distribution by Major")
    try:
        with st.spinner('Loading major distribution...'):
            response = requests.get('http://web-api:4000/a/analytics/students/major-distribution', timeout=2)
            if response.status_code == 200:
                data = response.json()
                if data['status'] == 'success' and 'distribution' in data:
                    distribution = data['distribution']
                    
                    # Create bar chart for major distribution
                    fig = go.Figure(data=[
                        go.Bar(
                            x=distribution.get('majors', []),
                            y=distribution.get('counts', []),
                            text=distribution.get('counts', []),
                            textposition='auto',
                        )
                    ])
                    
                    fig.update_layout(
                        title='',
                        xaxis_title='Major',
                        yaxis_title='Number of Students',
                        showlegend=False,
                        height=400,
                        margin=dict(t=0, b=0, l=0, r=0),
                        plot_bgcolor='white'
                    )
                    
                    fig.update_xaxes(tickangle=45)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("No data available for major distribution")
            else:
                st.error(f"Failed to fetch major distribution data: {response.text}")
    except Exception as e:
        st.error(f"Error loading major distribution: {str(e)}")

with col2:
    st.subheader("Student Matches Distribution")
    try:
        with st.spinner('Loading matches distribution...'):
            response = requests.get('http://web-api:4000/a/analytics/students/matches-distribution', timeout=2)
            if response.status_code == 200:
                data = response.json()
                if data['status'] == 'success' and 'distribution' in data:
                    distribution = data['distribution']
                    
                    # Create bar chart for matches distribution
                    fig = go.Figure(data=[
                        go.Bar(
                            x=distribution.get('categories', []),
                            y=distribution.get('counts', []),
                            text=distribution.get('counts', []),
                            textposition='auto',
                        )
                    ])
                    
                    fig.update_layout(
                        title='',
                        xaxis_title='Number of Matches',
                        yaxis_title='Number of Students',
                        showlegend=False,
                        height=400,
                        margin=dict(t=0, b=0, l=0, r=0),
                        plot_bgcolor='white'
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("No data available for matches distribution")
            else:
                st.error(f"Failed to fetch matches distribution data: {response.text}")
    except Exception as e:
        st.error(f"Error loading matches distribution: {str(e)}")