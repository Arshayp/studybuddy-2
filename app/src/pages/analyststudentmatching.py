import streamlit as st
import plotly.express as px
import pandas as pd
import requests
from modules.nav import setup_page

API_BASE_URL = "http://web-api:4000"

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
    
if st.sidebar.button("Geographic Data", use_container_width=True, key="nav_geographic_match"):
    st.switch_page("pages/analystgeographic.py")
    
if st.sidebar.button("Academic Insights", use_container_width=True, key="nav_academic_match"):
    st.switch_page("pages/analystacademic.py")

st.sidebar.divider()

# Main content
st.title("Student Matching Analytics")
st.write("Analyze compatibility factors and matching success rates")

# Function to fetch total matches
def get_total_matches():
    try:
        response = requests.get(f"{API_BASE_URL}/a/matches/total")
        if response.status_code == 200:
            data = response.json()
            return data.get('total_matches', 0)
        return None
    except Exception:
        return None

# Top metrics row
col1, col2, col3, col4 = st.columns(4)

# Fetch total matches
total_matches = get_total_matches()

with col1:
    if total_matches is not None:
        st.metric(
            "Total Matches",
            f"{total_matches:,}",
            "API available"
        )
    else:
        st.metric(
            "Total Matches",
            "0",
            "API unavailable"
        )

with col2:
    st.metric(
        "Success Rate",
        "87%",
        "+5% this month"
    )

with col3:
    st.metric(
        "Avg Match Time",
        "2.4 days",
        "-0.8 days"
    )

with col4:
    st.metric(
        "Active Pairs",
        "892",
        "Currently studying"
    )

# Create two columns for the visualizations
left_col, right_col = st.columns(2)

with left_col:
    st.subheader("Compatibility Matrix")
    
    # Sample compatibility data
    compatibility_data = pd.DataFrame({
        'Factor': ['Goals', 'Schedule', 'Learning Style'],
        'Score': [82, 90, 75]
    })
    
    # Create bar chart
    fig = px.bar(
        compatibility_data,
        x='Score',
        y='Factor',
        orientation='h',
        text=[f"{v}%" for v in compatibility_data['Score']]
    )
    
    fig.update_traces(
        marker_color='#1a1a2e',
        textposition='outside'
    )
    
    fig.update_layout(
        xaxis_range=[0, 100],
        showlegend=False,
        xaxis_title="",
        yaxis_title=""
    )
    
    st.plotly_chart(fig, use_container_width=True)

with right_col:
    st.subheader("Recent Successful Matches")
    
    # Display recent matches
    st.write("**Alex & Jordan**")
    st.write("Calculus II")
    st.write("95% compatible")
    st.divider()
    
    st.write("**Sam & Taylor**")
    st.write("Physics")
    st.write("88% compatible")

# Two main sections side by side
left_col, right_col = st.columns([3, 2])

with left_col:
    st.subheader("Compatibility Matrix")
    
    # Create compatibility data
    compatibility_data = pd.DataFrame({
        'Factor': ['Learning Style', 'Schedule', 'Goals'],
        'Percentage': [75, 90, 82]
    })
    
    # Create horizontal bar chart
    fig = px.bar(
        compatibility_data,
        x='Percentage',
        y='Factor',
        orientation='h',
        text=[f"{v}%" for v in compatibility_data['Percentage']],
    )
    
    fig.update_traces(
        marker_color='#1a1a2e',
        textposition='auto',
    )
    
    fig.update_layout(
        showlegend=False,
        xaxis_range=[0, 100],
        yaxis_title="",
        xaxis_title="",
        margin=dict(l=0, r=0, t=0, b=0),
        height=200
    )
    
    st.plotly_chart(fig, use_container_width=True)

with right_col:
    st.subheader("Recent Successful Matches")
    
    # Example matches
    matches = [
        {"pair": "Alex & Jordan", "course": "Calculus II", "compatibility": "95%"},
        {"pair": "Sam & Taylor", "course": "Physics", "compatibility": "88%"}
    ]
    
    for match in matches:
        with st.container():
            cols = st.columns([3, 1])
            with cols[0]:
                st.write(f"**{match['pair']}**")
                st.write(f"{match['course']}")
            with cols[1]:
                st.write(f"{match['compatibility']} compatible")
            st.divider() 