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
    
if st.sidebar.button("Geographic Data", use_container_width=True, key="nav_geographic_match"):
    st.switch_page("pages/analystgeographic.py")
    
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

# Top metrics in a row
col1, col2, col3, col4 = st.columns(4)

with col1:
    # Show loading spinner while fetching data
    with st.spinner('Fetching match data...'):
        try:
            response = requests.get('http://localhost:5000/api/matches/total', timeout=2)
            if response.status_code == 200:
                data = response.json()
                st.session_state.total_matches = data['total_matches']
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