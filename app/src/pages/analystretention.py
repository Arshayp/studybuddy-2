import streamlit as st
import plotly.express as px
import pandas as pd
import requests
from modules.nav import setup_page

API_BASE_URL = "http://web-api:4000"

# Page Configuration
st.set_page_config(
    page_title="StudyBuddy - Retention Analysis",
    page_icon="📊",
    layout="wide"
)

# Set current page in session state
st.session_state.page = 'analystretention'

# Initialize session state for retention metrics if not exists
if 'retention_rate' not in st.session_state:
    st.session_state.retention_rate = 0
    st.session_state.retention_change = "Loading..."
if 'active_members' not in st.session_state:
    st.session_state.active_members = 0
    st.session_state.members_change = "Loading..."

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
st.write("Track student engagement and identify patterns in study group longevity.")

# Helper function to fetch retention data
def get_retention_analytics():
    try:
        response = requests.get(f"{API_BASE_URL}/a/analytics/retention")  # Updated to include /a prefix
        if response.status_code == 200:
            return response.json(), None
        return None, f"API Error: {response.status_code}"
    except requests.exceptions.RequestException as e:
        return None, f"Connection Error: {str(e)}"

# Fetch data with loading state
with st.spinner('Fetching retention analytics...'):
    analytics_data, error = get_retention_analytics()

if error:
    st.error(f"Could not load retention analytics: {error}")

# Top metrics row
col1, col2, col3, col4 = st.columns(4)

with col1:
    # Show loading spinner while fetching data
    retention_rate = "86%"
    retention_change = "+3% vs last term"
    if analytics_data and 'retention_metrics' in analytics_data:
        retention_rate = analytics_data['retention_metrics'].get('overall_rate', retention_rate)
        retention_change = analytics_data['retention_metrics'].get('rate_change', retention_change)
    
    st.metric(
        "Overall Retention",
        retention_rate,
        retention_change
    )

with col2:
    lifespan = "4.2 months"
    lifespan_change = "+0.5 months"
    if analytics_data and 'group_metrics' in analytics_data:
        lifespan = analytics_data['group_metrics'].get('avg_lifespan', lifespan)
        lifespan_change = analytics_data['group_metrics'].get('lifespan_change', lifespan_change)
    
    st.metric(
        "Avg Group Lifespan",
        lifespan,
        lifespan_change
    )

with col3:
    active_members = "1,847"
    members_change = "+215 this term"
    if analytics_data and 'member_metrics' in analytics_data:
        active_members = analytics_data['member_metrics'].get('active_count', active_members)
        members_change = analytics_data['member_metrics'].get('count_change', members_change)
    
    st.metric(
        "Active Members",
        active_members,
        members_change
    )

with col4:
    at_risk = "12"
    risk_change = "-3 vs last month"
    if analytics_data and 'risk_metrics' in analytics_data:
        at_risk = analytics_data['risk_metrics'].get('at_risk_count', at_risk)
        risk_change = analytics_data['risk_metrics'].get('risk_change', risk_change)
    
    st.metric(
        "At-Risk Groups",
        at_risk,
        risk_change
    )

# Create two columns for the first row of charts
left_col, right_col = st.columns(2)

with left_col:
    st.subheader("Monthly Retention Rates")
    
    # Monthly retention data
    if analytics_data and 'monthly_retention' in analytics_data:
        monthly_data = pd.DataFrame(analytics_data['monthly_retention'])
    else:
        monthly_data = pd.DataFrame({
            'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
            'Retention Rate': [82, 84, 85, 86, 86, 87]
        })
    
    fig = px.line(
        monthly_data,
        x='Month',
        y='Retention Rate',
        markers=True
    )
    fig.update_traces(
        line_color='#1a1a2e',
        marker=dict(size=8)
    )
    fig.update_layout(
        yaxis_range=[75, 100],
        yaxis_title="Retention Rate (%)"
    )
    st.plotly_chart(fig, use_container_width=True)

with right_col:
    st.subheader("Group Size Distribution")
    
    # Group size data
    if analytics_data and 'size_distribution' in analytics_data:
        size_data = pd.DataFrame(analytics_data['size_distribution'])
    else:
        size_data = pd.DataFrame({
            'Size': ['2-3', '4-5', '6-7', '8+'],
            'Groups': [45, 32, 15, 8]
        })
    
    fig = px.pie(
        size_data,
        names='Size',
        values='Groups',
        color_discrete_sequence=['#1a1a2e', '#4a4a5a', '#8a8a9a', '#cccccc']
    )
    fig.update_traces(textinfo='percent+label')
    st.plotly_chart(fig, use_container_width=True)

# Create two columns for the second row
left_col2, right_col2 = st.columns(2)

with left_col2:
    st.subheader("Retention by Study Format")
    
    # Format retention data
    if analytics_data and 'format_retention' in analytics_data:
        format_data = pd.DataFrame(analytics_data['format_retention'])
    else:
        format_data = pd.DataFrame({
            'Format': ['In-Person', 'Hybrid', 'Virtual', 'Async'],
            'Retention': [92, 88, 82, 75]
        })
    
    fig = px.bar(
        format_data,
        x='Format',
        y='Retention',
        text=[f"{v}%" for v in format_data['Retention']],
        color='Format',
        color_discrete_sequence=['#1a1a2e', '#4a4a5a', '#8a8a9a', '#cccccc']
    )
    fig.update_traces(textposition='outside')
    fig.update_layout(
        showlegend=False,
        yaxis_range=[0, 100],
        yaxis_title="Retention Rate (%)"
    )
    st.plotly_chart(fig, use_container_width=True)

with right_col2:
    st.subheader("Member Activity Timeline")
    
    # Activity timeline data
    if analytics_data and 'member_activity' in analytics_data:
        timeline_data = pd.DataFrame(analytics_data['member_activity'])
    else:
        timeline_data = pd.DataFrame({
            'Week': list(range(1, 9)),
            'Active Members': [1500, 1600, 1680, 1720, 1780, 1800, 1830, 1847]
        })
    
    fig = px.line(
        timeline_data,
        x='Week',
        y='Active Members',
        markers=True
    )
    fig.update_traces(line_color='#1a1a2e')
    fig.update_layout(
        xaxis_title="Week of Term",
        yaxis_title="Active Members"
    )
    st.plotly_chart(fig, use_container_width=True)

# Risk Factors Section
st.subheader("Retention Risk Factors")

# Create three columns for risk factors
risk_col1, risk_col2, risk_col3 = st.columns(3)

with risk_col1:
    low_engagement = "5"
    if analytics_data and 'risk_factors' in analytics_data:
        low_engagement = str(analytics_data['risk_factors'].get('low_engagement', low_engagement))
    
    st.error("🚫 **Low Engagement**\nGroups with < 1 meeting/week")
    st.write(f"Affected Groups: {low_engagement}")

with risk_col2:
    declining_attendance = "4"
    if analytics_data and 'risk_factors' in analytics_data:
        declining_attendance = str(analytics_data['risk_factors'].get('declining_attendance', declining_attendance))
    
    st.warning("⚠️ **Declining Attendance**\n>20% drop in participation")
    st.write(f"Affected Groups: {declining_attendance}")

with risk_col3:
    schedule_conflicts = "3"
    if analytics_data and 'risk_factors' in analytics_data:
        schedule_conflicts = str(analytics_data['risk_factors'].get('schedule_conflicts', schedule_conflicts))
    
    st.info("ℹ️ **Schedule Conflicts**\nReported by 3+ members")
    st.write(f"Affected Groups: {schedule_conflicts}") 