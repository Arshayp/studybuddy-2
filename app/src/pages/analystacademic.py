import streamlit as st
import plotly.express as px
import pandas as pd
import requests
from modules.nav import setup_page

API_BASE_URL = "http://web-api:4000"

# Page Configuration
st.set_page_config(
    page_title="StudyBuddy - Academic Insights",
    page_icon="🎓",
    layout="wide"
)

# Set current page in session state
st.session_state.page = 'analystacademic'

# Setup page
setup_page("Academic Insights")

# Sidebar navigation
st.sidebar.title("Analytics Navigation")

if st.sidebar.button("Dashboard", use_container_width=True, key="nav_dashboard_acad"):
    st.switch_page("pages/dataanalystdashboard.py")
    
if st.sidebar.button("Student Matching", use_container_width=True, key="nav_matching_acad"):
    st.switch_page("pages/analyststudentmatching.py")
    
if st.sidebar.button("Retention Analysis", use_container_width=True, key="nav_retention_acad"):
    st.switch_page("pages/analystretention.py")
    
if st.sidebar.button("Academic Insights", use_container_width=True, key="nav_academic_acad"):
    st.switch_page("pages/analystacademic.py")

st.sidebar.divider()

# Main content
st.title("Academic Insights")
st.write("Explore course performance and cross-major participation analytics")

# Add real-time course performance analytics
st.subheader("Course Performance Analytics (Real-Time)")
try:
    response = requests.get(f"{API_BASE_URL}/a/analytics/academic/course-performance", timeout=5)
    
    if response.status_code == 200:
        data = response.json()
        if data and 'course_analytics' in data:
            # Convert to DataFrame for visualization
            df = pd.DataFrame(data['course_analytics'])
            
            if df.empty:
                st.warning("No course data available. This could be because there are no study sessions recorded yet.")
            else:
                # Create bar chart showing student participation by course
                fig = px.bar(
                    df,
                    x='course_name',
                    y='student_count',
                    color='department',
                    title='Student Participation by Course',
                    labels={
                        'course_name': 'Course',
                        'student_count': 'Number of Students',
                        'department': 'Department'
                    }
                )
                fig.update_layout(
                    xaxis_tickangle=-45,
                    plot_bgcolor='white',
                    height=400,
                    margin=dict(t=30, b=0, l=0, r=0)
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Show course metrics in an expander
                with st.expander("View Detailed Course Metrics"):
                    metrics_df = df[[
                        'department',
                        'course_name', 
                        'student_count',
                        'total_sessions',
                        'avg_sessions_per_student'
                    ]].sort_values('student_count', ascending=False)
                    
                    st.dataframe(metrics_df)
                
            # Show cross-major participation if available
            if 'major_distribution' in data:
                st.subheader("Cross-Major Course Participation")
                major_df = pd.DataFrame(data['major_distribution'])
                
                if not major_df.empty:
                    fig2 = px.bar(
                        major_df,
                        x='major',
                        y='course_count',
                        title='Number of Courses Taken by Major',
                        labels={
                            'major': 'Student Major',
                            'course_count': 'Number of Different Courses'
                        }
                    )
                    fig2.update_layout(
                        xaxis_tickangle=-45,
                        plot_bgcolor='white',
                        height=400,
                        margin=dict(t=30, b=0, l=0, r=0)
                    )
                    st.plotly_chart(fig2, use_container_width=True)
                else:
                    st.warning("No cross-major participation data available yet.")
        else:
            st.error("Response did not contain expected course analytics data structure")
    else:
        st.error(f"Could not load course performance analytics. Status code: {response.status_code}")
except Exception as e:
    st.error(f"Error loading course performance data: {str(e)}") 