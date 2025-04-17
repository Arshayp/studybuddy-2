import streamlit as st
from modules.nav import setup_page
import plotly.express as px
import pandas as pd
import requests

API_BASE_URL = "http://web-api:4000"

def normalize_learning_style(style):
    """Normalize the learning style string to match our expected values."""
    if not style:
        return "Visual"  # Default value
    # Convert to lowercase and strip any extra spaces
    style = style.lower().strip()
    # Map to our standard values
    style_map = {
        'visual': 'Visual',
        'auditory': 'Auditory',
        'reading/writing': 'Reading/Writing',
        'kinesthetic': 'Kinesthetic',
        'reading_writing': 'Reading/Writing',
        'reading writing': 'Reading/Writing'
    }
    return style_map.get(style, 'Visual')  # Default to Visual if unknown style

def get_user_learning_style(user_id):
    try:
        response = requests.get(f"{API_BASE_URL}/users/{user_id}")
        if response.status_code == 200:
            user_data = response.json()
            return user_data.get('learning_style')
        st.error(f"Error fetching learning style: {response.text}")
        return None
    except Exception as e:
        st.error(f"Error fetching learning style: {e}")
        return None

def get_learning_style_distribution(user_id):
    try:
        response = requests.get(f"{API_BASE_URL}/learning-style/distribution/{user_id}")
        if response.status_code == 200:
            data = response.json()
            return {
                'Style': ['Visual', 'Auditory', 'Reading/Writing', 'Kinesthetic'],
                'Percentage': [
                    data.get('visual_percentage', 0),
                    data.get('auditory_percentage', 0),
                    data.get('reading_writing_percentage', 0),
                    data.get('kinesthetic_percentage', 0)
                ]
            }
        st.error(f"Error fetching learning style distribution: {response.text}")
        return None
    except Exception as e:
        st.error(f"Error fetching learning style distribution: {e}")
        return None

def get_learning_profile(user_id):
    try:
        response = requests.get(f"{API_BASE_URL}/learning-style/profile/{user_id}")
        if response.status_code == 200:
            data = response.json()
            return {
                'strengths': data.get('strengths', '').split(', '),
                'areas_for_growth': data.get('areas_for_growth', '').split(', ')
            }
        st.error(f"Error fetching learning profile: {response.text}")
        return None
    except Exception as e:
        st.error(f"Error fetching learning profile: {e}")
        return None

def get_study_techniques(learning_style):
    try:
        response = requests.get(f"{API_BASE_URL}/learning-style/techniques/{learning_style}")
        if response.status_code == 200:
            data = response.json()
            return [item['technique_description'] for item in data]
        st.error(f"Error fetching study techniques: {response.text}")
        return []
    except Exception as e:
        st.error(f"Error fetching study techniques: {e}")
        return []

def get_study_tools(learning_style):
    try:
        response = requests.get(f"{API_BASE_URL}/learning-style/tools/{learning_style}")
        if response.status_code == 200:
            return response.json()
        st.error(f"Error fetching study tools: {response.text}")
        return []
    except Exception as e:
        st.error(f"Error fetching study tools: {e}")
        return []

def get_group_recommendations(learning_style):
    try:
        response = requests.get(f"{API_BASE_URL}/learning-style/recommendations/{learning_style}")
        if response.status_code == 200:
            data = response.json()
            return [item['recommendation_description'] for item in data]
        st.error(f"Error fetching group recommendations: {response.text}")
        return []
    except Exception as e:
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

# Get user ID from session
user_id = st.session_state.get('user', {}).get('id')
if not user_id:
    st.error("Please log in to view your learning style insights")
    st.stop()

# Get user's learning style
learning_style = get_user_learning_style(user_id)
if not learning_style:
    st.error("Could not fetch user's learning style")
    st.stop()

# Normalize the learning style
learning_style = normalize_learning_style(learning_style)

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
        ### {learning_style} Learner
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
        st.subheader(f"{learning_style} Learning Techniques")
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
        learning_styles = ["Visual", "Auditory", "Reading/Writing", "Kinesthetic"]
        try:
            current_index = learning_styles.index(learning_style)
        except ValueError:
            current_index = 0  # Default to first option if current style not found
            
        new_learning_style = st.selectbox(
            "Primary Learning Style",
            learning_styles,
            index=current_index
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
            try:
                response = requests.put(
                    f"{API_BASE_URL}/user/{user_id}",
                    json={
                        "learning_style": new_learning_style.lower(),
                        "preferences": preferences
                    }
                )
                if response.status_code == 200:
                    st.success("Your learning style preferences have been updated!")
                else:
                    st.error(f"Error updating preferences: {response.text}")
            except Exception as e:
                st.error(f"Error updating preferences: {e}")
            
    st.divider()
    
    # Learning style assessment
    st.subheader("Take a Learning Style Assessment")
    st.write("Not sure about your learning style? Take our quick assessment!")
    if st.button("Start Assessment"):
        st.info("Assessment feature coming soon!") 