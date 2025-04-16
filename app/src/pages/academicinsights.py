import streamlit as st
import requests
from modules.nav import setup_page

API_BASE_URL = "http://web-api:4000"

# Page Config
st.set_page_config(
    page_title="StudyBuddy - Academic Insights",
    page_icon="🎓",
    layout="wide"
)

# Basic setup
setup_page("Academic Insights")

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

st.title("Academic Insights")

# Fetch data
analytics_data, error = get_cohort_analytics()

if error:
    st.error(f"Could not load analytics data: {error}")
else:
    if analytics_data and 'sessions' in analytics_data:
        sessions = analytics_data['sessions']
        
        # Session activity metrics
        st.write("### Study Session Patterns")
        for session in sessions:
            st.write(f"**Course ID: {session['Course_ID']}**")
            st.write(f"Total Sessions: {session['session_count']}")
            st.write(f"Average Duration: {session['avg_duration']:.1f} days")
            st.divider()
    else:
        st.write("No session data available") 