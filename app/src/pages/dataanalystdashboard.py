import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
import requests
from modules.nav import setup_page

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

if st.sidebar.button("Dashboard", use_container_width=True, key="nav_dashboard"):
    st.switch_page("pages/dataanalystdashboard.py")
    
if st.sidebar.button("Student Matching", use_container_width=True, key="nav_matching"):
    st.switch_page("pages/analyststudentmatching.py")
    
if st.sidebar.button("Retention Analysis", use_container_width=True, key="nav_retention"):
    st.switch_page("pages/analystretention.py")
    
if st.sidebar.button("Geographic Data", use_container_width=True, key="nav_geographic"):
    st.switch_page("pages/analystgeographic.py")
    
if st.sidebar.button("Academic Insights", use_container_width=True, key="nav_academic"):
    st.switch_page("pages/analystacademic.py")

st.sidebar.divider()

# Main content
st.write("Welcome back, Sophia! Here's your analytics summary.")

# Initialize session state for retention if not exists
if 'retention_rate' not in st.session_state:
    st.session_state.retention_rate = 0
    st.session_state.retention_change = "Loading..."

# Top metrics row
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Active Study Groups",
        "2,047",
        "+12% vs last month"
    )

with col2:
    st.metric(
        "Avg. Session Score",
        "8.4/10",
        "+0.6 vs last month"
    )

with col3:
    # Show loading spinner while fetching data
    with st.spinner('Fetching retention data...'):
        try:
            response = requests.get('http://localhost:5000/a/analytics/retention', timeout=1)
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

with col4:
    st.metric(
        "At-Risk Students",
        "142",
        "-8% vs last month"
    )

# Create two columns for the charts
left_col, right_col = st.columns(2)

with left_col:
    st.subheader("Matching Success Rates")
    
    # Sample data for the bar chart
    categories = ['Success Rate', 'Learning Style', 'Schedule']
    values = [78, 92, 65]
    
    # Create bar chart using plotly
    fig = px.bar(
        x=categories,
        y=values,
        labels={'x': '', 'y': '%'},
        text=[f"{v}%" for v in values]
    )
    fig.update_traces(marker_color=['#000000', '#1a1a2e', '#2a2a3c'])
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

with right_col:
    st.subheader("Cohort Retention")
    
    # Sample retention data
    retention_data = pd.DataFrame({
        'Period': ['30d', '60d', '90d'],
        'Retention': [95, 85, 75]
    })
    
    # Create retention line chart
    fig = px.line(
        retention_data,
        x='Period',
        y='Retention',
        markers=True
    )
    fig.update_traces(line_color='#000000')
    st.plotly_chart(fig, use_container_width=True)

# Bottom row with two more visualizations
left_col2, right_col2 = st.columns(2)

with left_col2:
    st.subheader("Campus Study Hotspots")
    
    # Sample data for bubble chart
    np.random.seed(42)
    n_points = 3
    
    df = pd.DataFrame({
        'x': np.random.rand(n_points),
        'y': np.random.rand(n_points),
        'size': np.random.randint(30, 50, n_points),
        'activity': ['High Activity', 'Low Activity', 'Low Activity']
    })
    
    fig = px.scatter(
        df,
        x='x',
        y='y',
        size='size',
        color='activity',
        color_discrete_map={
            'High Activity': '#4a4a5a',
            'Low Activity': '#8a8a9a'
        }
    )
    fig.update_layout(
        xaxis_visible=False,
        yaxis_visible=False
    )
    st.plotly_chart(fig, use_container_width=True)

with right_col2:
    st.subheader("Course Difficulty Network")
    
    # Sample network data
    network_data = pd.DataFrame({
        'Course': ['Calculus', 'Physics', 'Chemistry'],
        'x': [0, 1, 0.5],
        'y': [0, 0, 1]
    })
    
    fig = px.scatter(
        network_data,
        x='x',
        y='y',
        text='Course',
        color_discrete_sequence=['#000000']
    )
    
    # Add lines between nodes
    for i in range(len(network_data)):
        for j in range(i+1, len(network_data)):
            fig.add_shape(
                type='line',
                x0=network_data.iloc[i]['x'],
                y0=network_data.iloc[i]['y'],
                x1=network_data.iloc[j]['x'],
                y1=network_data.iloc[j]['y'],
                line=dict(color='#cccccc', width=1)
            )
    
    fig.update_traces(marker=dict(size=12))
    fig.update_layout(
        xaxis_visible=False,
        yaxis_visible=False,
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)