import streamlit as st
from modules.nav import setup_page
import plotly.express as px
import pandas as pd
import mysql.connector
from mysql.connector import Error

# Database connection configuration
DB_CONFIG = {
    'host': 'mysql_db',
    'user': 'root',
    'password': 'Vaish0208',
    'database': 'study_buddy_system'
}

def get_db_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        st.error(f"Error connecting to database: {e}")
        return None

def get_user_learning_style(user_id):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            
            # Get user's learning style
            cursor.execute("""
                SELECT learning_style 
                FROM user 
                WHERE userid = %s
            """, (user_id,))
            result = cursor.fetchone()
            
            cursor.close()
            conn.close()
            return result['learning_style'] if result else None
        except Error as e:
            st.error(f"Error fetching learning style: {e}")
            return None

def get_learning_style_distribution(user_id):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            
            # Get learning style distribution
            cursor.execute("""
                SELECT visual_percentage, auditory_percentage, 
                       reading_writing_percentage, kinesthetic_percentage 
                FROM learning_style_distribution 
                WHERE userid = %s
            """, (user_id,))
            result = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            if result:
                return {
                    'Style': ['Visual', 'Auditory', 'Reading/Writing', 'Kinesthetic'],
                    'Percentage': [
                        result['visual_percentage'],
                        result['auditory_percentage'],
                        result['reading_writing_percentage'],
                        result['kinesthetic_percentage']
                    ]
                }
            return None
        except Error as e:
            st.error(f"Error fetching learning style distribution: {e}")
            return None

def get_learning_profile(user_id):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            
            # Get learning profile
            cursor.execute("""
                SELECT strengths, areas_for_growth 
                FROM learning_style_profile 
                WHERE userid = %s
            """, (user_id,))
            result = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            if result:
                return {
                    'strengths': result['strengths'].split(', '),
                    'areas_for_growth': result['areas_for_growth'].split(', ')
                }
            return None
        except Error as e:
            st.error(f"Error fetching learning profile: {e}")
            return None

def get_study_techniques(learning_style):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            
            # Get study techniques
            cursor.execute("""
                SELECT technique_description 
                FROM study_techniques 
                WHERE learning_style = %s
            """, (learning_style,))
            results = cursor.fetchall()
            
            cursor.close()
            conn.close()
            
            return [result['technique_description'] for result in results]
        except Error as e:
            st.error(f"Error fetching study techniques: {e}")
            return []

def get_study_tools(learning_style):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            
            # Get study tools
            cursor.execute("""
                SELECT tool_name, tool_description 
                FROM study_tools 
                WHERE learning_style = %s
            """, (learning_style,))
            results = cursor.fetchall()
            
            cursor.close()
            conn.close()
            
            return results
        except Error as e:
            st.error(f"Error fetching study tools: {e}")
            return []

def get_group_recommendations(learning_style):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            
            # Get group recommendations
            cursor.execute("""
                SELECT recommendation_description 
                FROM study_group_recommendations 
                WHERE learning_style = %s
            """, (learning_style,))
            results = cursor.fetchall()
            
            cursor.close()
            conn.close()
            
            return [result['recommendation_description'] for result in results]
        except Error as e:
            st.error(f"Error fetching group recommendations: {e}")
            return []

# Page Configuration
st.set_page_config(
    page_title="StudyBuddy - Learning Style Insights",
    page_icon="🧠",
    layout="wide"
)

# Setup
setup_page("Learning Style Insights")

# User Information
st.title("🧠 Learning Style Insights")

# TODO: Replace with actual user ID from session
user_id = 1  # Example user ID

# Get user's learning style
learning_style = get_user_learning_style(user_id)
if not learning_style:
    st.error("Could not fetch user's learning style")
    st.stop()

# Create tabs for different sections
style_tab, tips_tab, update_tab = st.tabs([
    "Your Learning Style", 
    "Study Tips", 
    "Update Preferences"
])

# Learning Style Tab
with style_tab:
    st.header("Your Learning Style Profile")
    
    # Create columns for style information
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Primary Learning Style")
        st.markdown(f"""
        ### {learning_style.title()} Learner
        """)
        
        # Learning style distribution chart
        st.subheader("Learning Style Distribution")
        distribution_data = get_learning_style_distribution(user_id)
        if distribution_data:
            df = pd.DataFrame(distribution_data)
            fig = px.pie(df, values='Percentage', names='Style', 
                        title='Your Learning Style Distribution',
                        color_discrete_sequence=px.colors.qualitative.Pastel)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        profile = get_learning_profile(user_id)
        if profile:
            st.subheader("Strengths")
            for strength in profile['strengths']:
                st.write(f"✅ {strength}")
            
            st.subheader("Areas for Growth")
            for area in profile['areas_for_growth']:
                st.write(f"📈 {area}")

# Study Tips Tab
with tips_tab:
    st.header("📚 Recommended Study Techniques")
    
    # Create columns for different types of tips
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(f"{learning_style.title()} Learning Techniques")
        techniques = get_study_techniques(learning_style)
        for technique in techniques:
            st.write(f"🎨 {technique}")
    
    with col2:
        st.subheader("Study Tools Recommendations")
        tools = get_study_tools(learning_style)
        for tool in tools:
            st.write(f"🛠️ {tool['tool_name']}: {tool['tool_description']}")
    
    st.divider()
    
    st.subheader("Study Group Recommendations")
    st.write("Based on your learning style, we recommend study groups that:")
    recommendations = get_group_recommendations(learning_style)
    for rec in recommendations:
        st.write(f"👥 {rec}")

# Update Preferences Tab
with update_tab:
    st.header("🔄 Update Your Learning Style Preferences")
    
    with st.form("learning_style_form"):
        st.write("Update your learning style preferences to get more personalized recommendations")
        
        # Learning style selection
        new_learning_style = st.selectbox(
            "Primary Learning Style",
            ["Visual", "Auditory", "Reading/Writing", "Kinesthetic"],
            index=["Visual", "Auditory", "Reading/Writing", "Kinesthetic"].index(learning_style.title())
        )
        
        # Additional preferences
        st.subheader("Additional Preferences")
        preferences = {
            "Study Environment": st.multiselect(
                "Preferred Study Environments",
                ["Quiet Library", "Coffee Shop", "Study Group", "Home", "Outdoors"]
            ),
            "Study Time": st.multiselect(
                "Preferred Study Times",
                ["Morning", "Afternoon", "Evening", "Night"]
            ),
            "Study Tools": st.multiselect(
                "Preferred Study Tools",
                ["Digital Notes", "Physical Notes", "Flashcards", "Videos", "Diagrams"]
            )
        }
        
        # Submit button
        if st.form_submit_button("Update Preferences"):
            conn = get_db_connection()
            if conn:
                try:
                    cursor = conn.cursor()
                    
                    # Update user's learning style
                    cursor.execute("""
                        UPDATE user 
                        SET learning_style = %s 
                        WHERE userid = %s
                    """, (new_learning_style.lower(), user_id))
                    
                    conn.commit()
                    cursor.close()
                    conn.close()
                    
                    st.success("Your learning style preferences have been updated!")
                except Error as e:
                    st.error(f"Error updating preferences: {e}")
            
    st.divider()
    
    # Learning style assessment
    st.subheader("Take a Learning Style Assessment")
    st.write("Not sure about your learning style? Take our quick assessment!")
    if st.button("Start Assessment"):
        st.info("Assessment feature coming soon!") 