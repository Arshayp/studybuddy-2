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
    
if st.sidebar.button("Geographic Data", use_container_width=True, key="nav_geographic_acad"):
    st.switch_page("pages/analystgeographic.py")
    
if st.sidebar.button("Academic Insights", use_container_width=True, key="nav_academic_acad"):
    st.switch_page("pages/analystacademic.py")

st.sidebar.divider()

# Main content
st.title("Academic Insights")
st.write("Explore academic performance trends and learning outcomes across courses.")

# Helper function to fetch analytics data
def get_academic_analytics():
    try:
        response = requests.get(f"{API_BASE_URL}/study/academic-analytics")
        if response.status_code == 200:
            return response.json()
        return None
    except Exception:
        return None

# Fetch data
analytics_data = get_academic_analytics()

# Top metrics row
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Average GPA",
        "3.42",
        "+0.08 vs last term"
    )

with col2:
    st.metric(
        "Pass Rate",
        "92%",
        "+2% vs last term"
    )

with col3:
    st.metric(
        "Study Hours/Week",
        "15.5",
        "+1.2 hours"
    )

with col4:
    st.metric(
        "Active Courses",
        "24",
        "+3 this term"
    )

# Create two columns for the first row of charts
left_col, right_col = st.columns(2)

with left_col:
    st.subheader("Top Performing Courses")
    
    # Course performance data
    course_data = pd.DataFrame({
        'Course': ['Calculus II', 'Physics 101', 'Chemistry', 'Biology'],
        'Average Grade': [92, 88, 85, 83]
    })
    
    fig = px.bar(
        course_data,
        x='Course',
        y='Average Grade',
        text=[f"{v}%" for v in course_data['Average Grade']],
        color='Course',
        color_discrete_sequence=['#1a1a2e', '#4a4a5a', '#8a8a9a', '#cccccc']
    )
    fig.update_traces(textposition='outside')
    fig.update_layout(
        showlegend=False,
        xaxis_title="",
        yaxis_title="Average Grade",
        yaxis_range=[0, 100]
    )
    st.plotly_chart(fig, use_container_width=True)

with right_col:
    st.subheader("Grade Distribution")
    
    # Grade distribution data
    grade_data = pd.DataFrame({
        'Grade': ['A', 'B', 'C', 'D', 'F'],
        'Students': [45, 30, 15, 7, 3]
    })
    
    fig = px.pie(
        grade_data,
        names='Grade',
        values='Students',
        color_discrete_sequence=['#1a1a2e', '#4a4a5a', '#8a8a9a', '#cccccc', '#e0e0e0']
    )
    fig.update_traces(textinfo='percent+label')
    st.plotly_chart(fig, use_container_width=True)

# Create two columns for the second row
left_col2, right_col2 = st.columns(2)

with left_col2:
    st.subheader("Study Time vs. Performance")
    
    # Study time vs performance data
    study_data = pd.DataFrame({
        'Hours': [5, 10, 15, 20, 25],
        'Average Grade': [75, 82, 88, 92, 95]
    })
    
    fig = px.scatter(
        study_data,
        x='Hours',
        y='Average Grade',
        labels={'Hours': 'Weekly Study Hours', 'Average Grade': 'Average Grade (%)'}
    )
    fig.update_traces(marker=dict(color='#1a1a2e', size=10))
    fig.update_layout(
        xaxis_title="Weekly Study Hours",
        yaxis_title="Average Grade (%)",
        yaxis_range=[70, 100]
    )
    st.plotly_chart(fig, use_container_width=True)

with right_col2:
    st.subheader("Learning Progress Over Time")
    
    # Learning progress data
    progress_data = pd.DataFrame({
        'Week': list(range(1, 11)),
        'Average Score': [70, 75, 78, 82, 85, 87, 88, 90, 91, 92]
    })
    
    fig = px.line(
        progress_data,
        x='Week',
        y='Average Score',
        markers=True,
        labels={'Week': 'Week Number', 'Average Score': 'Average Score (%)'}
    )
    fig.update_traces(line_color='#1a1a2e')
    st.plotly_chart(fig, use_container_width=True)

# Additional insights section
st.subheader("Key Academic Insights")

# Create three columns for insights
insight_col1, insight_col2, insight_col3 = st.columns(3)

with insight_col1:
    st.info("📚 Most Improved Subject: **Physics 101** with +5.2% increase in average grade")

with insight_col2:
    st.warning("⚠️ Challenging Area: **Organic Chemistry** with 68% pass rate")

with insight_col3:
    st.success("🎯 Best Study Pattern: **2-hour sessions** with 94% retention rate")

# Add real-time course performance analytics
st.subheader("Course Performance Analytics (Real-Time)")
try:
    st.write("Fetching course performance data...")
    response = requests.get(f"{API_BASE_URL}/a/analytics/academic/course-performance")
    st.write(f"API Response Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        st.write(f"Data received: {len(data.get('course_analytics', [])) if data and 'course_analytics' in data else 0} courses")
        
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
                fig.update_layout(xaxis_tickangle=-45)
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
                    
                # Display key insights
                # Most popular course
                popular_course = df.iloc[df['student_count'].idxmax()]
                st.info(f"📚 Most Popular Course: **{popular_course['course_name']}** "
                       f"({popular_course['department']}) with {popular_course['student_count']} students")
                
                # Most active department
                dept_stats = df.groupby('department').agg({
                    'student_count': 'sum',
                    'total_sessions': 'sum'
                }).reset_index()
                active_dept = dept_stats.iloc[dept_stats['total_sessions'].idxmax()]
                st.success(f"🎯 Most Active Department: **{active_dept['department']}** "
                         f"with {active_dept['total_sessions']} total study sessions")
                
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
                    fig2.update_layout(xaxis_tickangle=-45)
                    st.plotly_chart(fig2, use_container_width=True)
                else:
                    st.warning("No cross-major participation data available yet.")
        else:
            st.error("Response did not contain expected course analytics data structure")
            if data:
                st.write("Response structure:", data.keys())
    else:
        st.error(f"Could not load course performance analytics. Status code: {response.status_code}")
        try:
            error_data = response.json()
            st.write("Error details:", error_data)
        except:
            st.write("Could not parse error response")
except Exception as e:
    st.error(f"Error loading course performance data: {str(e)}")
    st.write("Stack trace:", e.__traceback__) 