import streamlit as st
import requests
import pandas as pd
from modules.nav import setup_page

API_BASE_URL = "http://web-api:4000"

# Page Config
st.set_page_config(
    page_title="StudyBuddy Analytics",
    page_icon="📊",
    layout="wide"
)

# Basic setup
setup_page("Analytics")

# Helper function to fetch analytics data
def get_cohort_analytics():
    try:
        response = requests.get(f"{API_BASE_URL}/s/cohort-analytics")
        if response.status_code == 200:
            return response.json(), None
        else:
            return None, f"API Error: {response.status_code} - {response.text}"
    except Exception as e:
        return None, f"Error fetching analytics: {str(e)}"

st.title("Analytics Dashboard")

# Fetch data once for both views
analytics_data, error = get_cohort_analytics()

if error:
    st.error(f"Could not load analytics data: {error}")
else:
    # Create tabs for different views
    tab1, tab2 = st.tabs(["Retention Analytics", "Academic Insights"])
    
    # Retention Analytics Tab
    with tab1:
        st.title("Retention Analytics")
        
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
    
    # Academic Insights Tab
    with tab2:
        st.title("Academic Insights")
        
        if analytics_data and 'sessions' in analytics_data:
            sessions = analytics_data['sessions']
            
            # Convert to DataFrame for better visualization
            df_sessions = pd.DataFrame(sessions)
            
            # Display course activity metrics
            st.write("### Course Activity Metrics")
            
            # Create columns for metrics
            col1, col2 = st.columns(2)
            
            with col1:
                # Bar chart for session counts
                st.subheader("Sessions per Course")
                if not df_sessions.empty:
                    st.bar_chart(
                        df_sessions.set_index('Course_Name')['session_count'],
                        use_container_width=True
                    )
                
            with col2:
                # Active students metrics
                st.subheader("Student Engagement")
                if not df_sessions.empty:
                    total_sessions = df_sessions['session_count'].sum()
                    total_active = df_sessions['active_students'].sum()
                    
                    st.metric("Total Study Sessions", total_sessions)
                    st.metric("Total Active Students", total_active)
                    if len(df_sessions) > 0:
                        avg_sessions = total_sessions / len(df_sessions)
                        st.metric("Average Sessions per Course", f"{avg_sessions:.1f}")
        else:
            st.info("No session data available") 