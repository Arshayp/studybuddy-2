import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import requests
from datetime import datetime
from modules.nav import setup_page

# Page Configuration
st.set_page_config(
    page_title="Retention Analysis",
    page_icon="📊",
    layout="wide"
)

# Set current page in session state
st.session_state.page = 'analystretention'

# Setup page
setup_page("Retention Analysis")

# Navigation in sidebar
st.sidebar.title("Analytics Navigation")

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
st.title("Match Creation Timeline")
st.write("Track when matches were created over time")

# Fetch match timeline data
with st.spinner('Loading match timeline data...'):
    try:
        response = requests.get('http://web-api:4000/a/analytics/matches/timeline', timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success' and data.get('timeline'):
                # Convert timeline data to DataFrame
                df = pd.DataFrame(data['timeline'])
                df['date'] = pd.to_datetime(df['date'])
                df = df.sort_values('date')
                
                # Create bar chart
                fig = go.Figure()
                fig.add_trace(go.Bar(
                    x=df['date'],
                    y=df['matches'],
                    marker_color='#1a1a2e',
                    hovertemplate='%{x|%Y-%m-%d}<br>Matches: %{y}<extra></extra>'
                ))
                
                # Update layout
                fig.update_layout(
                    title='Matches Created per Day',
                    xaxis_title='Date',
                    yaxis_title='Number of Matches',
                    showlegend=False,
                    plot_bgcolor='white',
                    height=500,
                    margin=dict(t=30, b=0, l=0, r=0)
                )
                
                # Update axes
                fig.update_xaxes(
                    showgrid=True,
                    gridwidth=1,
                    gridcolor='#f0f0f0'
                )
                fig.update_yaxes(
                    showgrid=True,
                    gridwidth=1,
                    gridcolor='#f0f0f0'
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Display summary statistics
                st.subheader("Match Statistics")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    total_matches = df['matches'].sum()
                    st.metric("Total Matches", total_matches)
                
                with col2:
                    first_match = df['date'].min().strftime('%Y-%m-%d')
                    st.metric("First Match", first_match)
                
                with col3:
                    last_match = df['date'].max().strftime('%Y-%m-%d')
                    st.metric("Latest Match", last_match)
            else:
                st.error("No timeline data available in the response.")
        else:
            st.error(f"Failed to fetch match data. Status code: {response.status_code}")
    except requests.exceptions.Timeout:
        st.error("Request timed out while fetching match data. Please try again.")
    except requests.exceptions.RequestException as e:
        st.error(f"Error loading match timeline data: {str(e)}") 