import streamlit as st
import requests
from modules.nav import setup_page

API_BASE_URL = "http://web-api:4000"

# Page Config
st.set_page_config(
    page_title="StudyBuddy - Retention Analytics",
    page_icon="📊",
    layout="wide"
)

# Basic setup
setup_page("Retention Analytics")

# Helper function to fetch analytics data
def get_cohort_analytics():
    try:
        response = requests.get(f"{API_BASE_URL}/study/cohort-analytics")
        if response.status_code == 200:
            return response.json(), None
        else:
            return None, f"API Error: {response.status_code} - {response.text}"
    except Exception as e:
        return None, f"Error fetching analytics: {str(e)}"

st.title("Retention Analytics")

# Fetch data
analytics_data, error = get_cohort_analytics()

if error:
    st.error(f"Could not load analytics data: {error}")
else:
    if analytics_data and 'groups' in analytics_data:
        groups = analytics_data['groups']
        
        # Group longevity metrics
        st.write("### Study Group Retention")
        for group in groups:
            st.write(f"**{group['Group_Name']}**")
            st.write(f"Created: {group['Created_At']}")
            st.write(f"Current Members: {group['member_count']}")
            st.write(f"Last Member Joined: {group['last_join_date']}")
            st.divider()
    else:
        st.write("No group data available")