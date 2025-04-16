import streamlit as st
<<<<<<< HEAD
import requests
import pandas as pd
import plotly.express as px
from modules.nav import setup_page

API_BASE_URL = "http://web-api:4000"

# Page Config
=======
import plotly.express as px
import pandas as pd
from modules.nav import setup_page

# Page Configuration
>>>>>>> d2376b76ce1618b0f85fa0ca5d270dd5c7bcccc5
st.set_page_config(
    page_title="Academic Insights",
    page_icon="🎓",
    layout="wide"
)

# Set current page in session state
st.session_state.page = 'analystacademic'

<<<<<<< HEAD
# Basic setup
=======
# Setup page
>>>>>>> d2376b76ce1618b0f85fa0ca5d270dd5c7bcccc5
setup_page("Academic Insights")

# Sidebar navigation
st.sidebar.title("Analytics Navigation")

if st.sidebar.button("Dashboard", use_container_width=True, key="nav_dashboard_acad"):
    st.switch_page("pages/dataanalystdashboard.py")
    
if st.sidebar.button("Student Matching", use_container_width=True, key="nav_matching_acad"):
    st.switch_page("pages/analyststudentmatching.py")
    
if st.sidebar.button("Retention Analysis", use_container_width=True, key="nav_retention_acad"):
    st.switch_page("pages/analystretention.py")
    
if st.sidebar.button("Geographic Data", use_container_width=True, key="nav_geographic_acad"):
    st.switch_page("pages/analystgeographic.py")
    
if st.sidebar.button("Academic Insights", use_container_width=True, key="nav_academic_acad"):
    st.switch_page("pages/analystacademic.py")

st.sidebar.divider()

# Main content
st.title("Academic Insights")
st.write("Explore academic performance trends and insights across courses and cohorts.")

<<<<<<< HEAD
# Helper function to fetch analytics data
def get_cohort_analytics():
    try:
        response = requests.get(f"{API_BASE_URL}/study/cohort-analytics")
        if response.status_code == 200:
            return response.json()
        return None
    except Exception:
        return None

# Fetch data silently (without showing errors)
analytics_data = get_cohort_analytics()

=======
>>>>>>> d2376b76ce1618b0f85fa0ca5d270dd5c7bcccc5
# Top metrics row
col1, col2 = st.columns(2)

with col1:
<<<<<<< HEAD
    gpa = "3.42"
    gpa_change = "+0.08 vs last term"
    if analytics_data and 'academic_metrics' in analytics_data:
        gpa = str(analytics_data['academic_metrics'].get('avg_gpa', gpa))
        gpa_change = analytics_data['academic_metrics'].get('gpa_change', gpa_change)
    
    st.metric(
        "Avg. GPA",
        gpa,
        gpa_change
    )

with col2:
    high_pass = "12"
    pass_change = "+2 vs last term"
    if analytics_data and 'academic_metrics' in analytics_data:
        high_pass = str(analytics_data['academic_metrics'].get('high_pass_courses', high_pass))
        pass_change = analytics_data['academic_metrics'].get('pass_rate_change', pass_change)
    
    st.metric(
        "Courses Above 90% Pass Rate",
        high_pass,
        pass_change
    )

# Top Performing Courses
st.subheader("Top Performing Courses")

if analytics_data and 'course_performance' in analytics_data:
    courses = pd.DataFrame(analytics_data['course_performance'])
else:
    # Demo data if API data is not available
    courses = pd.DataFrame({
        'Course': ['Calculus', 'Biology', 'Physics', 'Chemistry'],
        'Avg Grade': [91, 89, 87, 85]
    })

=======
    st.metric(
        "Avg. GPA",
        "3.42",
        "+0.08 vs last term"
    )

with col2:
    st.metric(
        "Courses Above 90% Pass Rate",
        "12",
        "+2 vs last term"
    )

# Simple bar chart: Top Performing Courses
st.subheader("Top Performing Courses")
courses = pd.DataFrame({
    'Course': ['Calculus', 'Biology', 'Physics', 'Chemistry'],
    'Avg Grade': [91, 89, 87, 85]
})
>>>>>>> d2376b76ce1618b0f85fa0ca5d270dd5c7bcccc5
fig = px.bar(
    courses,
    x='Course',
    y='Avg Grade',
    text='Avg Grade',
    color='Course',
    color_discrete_sequence=['#1a1a2e', '#4a4a5a', '#8a8a9a', '#cccccc']
)
fig.update_traces(texttemplate='%{text}', textposition='outside')
fig.update_layout(showlegend=False, yaxis_range=[0, 100])
st.plotly_chart(fig, use_container_width=True)

<<<<<<< HEAD
# Grade Distribution
st.subheader("Grade Distribution")

if analytics_data and 'grade_distribution' in analytics_data:
    grade_dist = pd.DataFrame(analytics_data['grade_distribution'])
else:
    # Demo data if API data is not available
    grade_dist = pd.DataFrame({
        'Grade': ['A', 'B', 'C', 'D', 'F'],
        'Count': [120, 95, 60, 15, 5]
    })

=======
# Simple pie chart: Grade Distribution
st.subheader("Grade Distribution")
grade_dist = pd.DataFrame({
    'Grade': ['A', 'B', 'C', 'D', 'F'],
    'Count': [120, 95, 60, 15, 5]
})
>>>>>>> d2376b76ce1618b0f85fa0ca5d270dd5c7bcccc5
fig2 = px.pie(
    grade_dist,
    names='Grade',
    values='Count',
    color_discrete_sequence=['#1a1a2e', '#4a4a5a', '#8a8a9a', '#cccccc', '#e0e0e0']
)
fig2.update_traces(textinfo='percent+label')
st.plotly_chart(fig2, use_container_width=True) 