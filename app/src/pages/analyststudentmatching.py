import streamlit as st
import plotly.express as px
import pandas as pd
import requests
from modules.nav import setup_page

# Page Configuration
st.set_page_config(
    page_title="Student Matching Analytics",
    page_icon="🤝",
    layout="wide"
)

# Set current page in session state
st.session_state.page = 'analyststudentmatching'

# Setup page
setup_page("Student Matching Analytics")

# Navigation in sidebar
st.sidebar.title("Analytics Navigation")

if st.sidebar.button("Dashboard", use_container_width=True, key="nav_dashboard_match"):
    st.switch_page("pages/dataanalystdashboard.py")
    
if st.sidebar.button("Student Matching", use_container_width=True, key="nav_matching_match"):
    st.switch_page("pages/analyststudentmatching.py")
    
if st.sidebar.button("Retention Analysis", use_container_width=True, key="nav_retention_match"):
    st.switch_page("pages/analystretention.py")
    
if st.sidebar.button("Academic Insights", use_container_width=True, key="nav_academic_match"):
    st.switch_page("pages/analystacademic.py")

st.sidebar.divider()

# Main content
st.title("Student Matching Analytics")
st.write("Analyze compatibility factors and matching success rates")

# Initialize session state for matches if not exists
if 'total_matches' not in st.session_state:
    st.session_state.total_matches = 0
    st.session_state.time_period = "Loading..."

if 'success_rate' not in st.session_state:
    st.session_state.success_rate = 0
    st.session_state.success_rate_change = 0

if 'avg_match_time' not in st.session_state:
    st.session_state.avg_match_time = 0
    st.session_state.avg_match_time_change = 0

# Top metrics in a row
col1, col2, col3 = st.columns(3)

with col1:
    # Show loading spinner while fetching data
    with st.spinner('Fetching total matches...'):
        try:
            response = requests.get('http://web-api:4000/a/matches/total', timeout=2)
            if response.status_code == 200:
                data = response.json()
                st.session_state.total_matches = data.get('total_matches', 0)
                st.session_state.time_period = data['time_period']
            else:
                st.session_state.total_matches = 0
                st.session_state.time_period = "Error fetching data"
        except requests.exceptions.RequestException:
            st.session_state.total_matches = 0
            st.session_state.time_period = "API unavailable"
    
    st.metric(
        "Total Matches",
        f"{st.session_state.total_matches:,}",
        st.session_state.time_period
    )

with col2:
    # Fetch success rate
    with st.spinner('Fetching success rate...'):
        try:
            response = requests.get('http://web-api:4000/a/analytics/matching/success-rate', timeout=2)
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'success':
                    st.session_state.success_rate = data.get('success_rate', 0)
                    st.session_state.success_rate_change = data.get('change', 0)
        except requests.exceptions.RequestException:
            pass
    
    st.metric(
        "Success Rate",
        f"{st.session_state.success_rate}%",
        f"{st.session_state.success_rate_change:+}% this month"
    )

with col3:
    # Fetch average match time
    with st.spinner('Fetching match time...'):
        try:
            response = requests.get('http://web-api:4000/a/analytics/matching/avg-time', timeout=2)
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'success':
                    st.session_state.avg_match_time = data.get('avg_days', 0)
                    st.session_state.avg_match_time_change = data.get('change', 0)
        except requests.exceptions.RequestException:
            pass
    
    st.metric(
        "Avg Match Time",
        f"{st.session_state.avg_match_time} days",
        f"{st.session_state.avg_match_time_change:+.1f} days"
    )

# Recent matches section
st.subheader("3 Most Recent Matches")

# Fetch recent matches
with st.spinner('Loading recent matches...'):
    try:
        response = requests.get('http://web-api:4000/a/analytics/matching/recent-matches', timeout=2)
        if response.status_code == 200:
            data = response.json()
            if data['status'] == 'success' and data['matches']:
                for match in data['matches']:
                    with st.container():
                        cols = st.columns([3, 2, 1])
                        with cols[0]:
                            st.write(f"**{match['pair']}**")
                            st.write(f"📚 {match['course']}")
                        with cols[1]:
                            st.write("🤝 Compatibility")
                            st.write(f"**{match['compatibility']}**")
                        with cols[2]:
                            st.write("📅 Matched on")
                            st.write(f"**{match['match_date']}**")
                        st.divider()
            else:
                st.info("No recent matches found")
    except Exception as e:
        st.error(f"Error loading recent matches: {str(e)}") 