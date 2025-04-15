import streamlit as st
from modules.nav import setup_page
import plotly.express as px
import pandas as pd

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
        st.markdown("""
        ### Visual Learner
        - You learn best through visual aids
        - Prefer diagrams, charts, and color-coded notes
        - Strong spatial understanding
        """)
        
        # Learning style distribution chart
        st.subheader("Learning Style Distribution")
        data = {
            'Style': ['Visual', 'Auditory', 'Reading/Writing', 'Kinesthetic'],
            'Percentage': [65, 15, 10, 10]
        }
        df = pd.DataFrame(data)
        fig = px.pie(df, values='Percentage', names='Style', 
                    title='Your Learning Style Distribution',
                    color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Strengths")
        strengths = [
            "Excellent at creating and interpreting visual representations",
            "Strong memory for images and spatial relationships",
            "Good at recognizing patterns and relationships",
            "Effective at organizing information visually"
        ]
        for strength in strengths:
            st.write(f"✅ {strength}")
        
        st.subheader("Areas for Growth")
        growth_areas = [
            "Developing auditory learning techniques",
            "Improving note-taking in lecture settings",
            "Enhancing verbal communication of ideas"
        ]
        for area in growth_areas:
            st.write(f"📈 {area}")

# Study Tips Tab
with tips_tab:
    st.header("📚 Recommended Study Techniques")
    
    # Create columns for different types of tips
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Visual Learning Techniques")
        techniques = [
            "Use mind maps and concept diagrams",
            "Create color-coded notes and flashcards",
            "Watch educational videos and animations",
            "Draw diagrams to explain concepts",
            "Use highlighters to organize information"
        ]
        for technique in techniques:
            st.write(f"🎨 {technique}")
    
    with col2:
        st.subheader("Study Tools Recommendations")
        tools = [
            "MindMeister for mind mapping",
            "Canva for creating visual notes",
            "Lucidchart for diagrams",
            "Quizlet for visual flashcards",
            "Khan Academy for video lessons"
        ]
        for tool in tools:
            st.write(f"🛠️ {tool}")
    
    st.divider()
    
    st.subheader("Study Group Recommendations")
    st.write("Based on your learning style, we recommend study groups that:")
    recommendations = [
        "Include visual learners for collaborative diagramming",
        "Use whiteboards or digital drawing tools",
        "Share visual resources and study materials",
        "Incorporate visual presentations in group study"
    ]
    for rec in recommendations:
        st.write(f"👥 {rec}")

# Update Preferences Tab
with update_tab:
    st.header("🔄 Update Your Learning Style Preferences")
    
    with st.form("learning_style_form"):
        st.write("Update your learning style preferences to get more personalized recommendations")
        
        # Learning style selection
        learning_style = st.selectbox(
            "Primary Learning Style",
            ["Visual", "Auditory", "Reading/Writing", "Kinesthetic"],
            index=0
        )
        
        # Additional preferences
        st.subheader("Additional Preferences")
        preferences = {
            "Study Environment": st.multiselect(
                "Preferred Study Environments",
                ["Quiet Library", "Coffee Shop", "Study Group", "Home", "Outdoors"],
                default=["Quiet Library", "Study Group"]
            ),
            "Study Time": st.multiselect(
                "Preferred Study Times",
                ["Morning", "Afternoon", "Evening", "Night"],
                default=["Morning", "Evening"]
            ),
            "Study Tools": st.multiselect(
                "Preferred Study Tools",
                ["Digital Notes", "Physical Notes", "Flashcards", "Videos", "Diagrams"],
                default=["Digital Notes", "Diagrams"]
            )
        }
        
        # Submit button
        if st.form_submit_button("Update Preferences"):
            st.success("Your learning style preferences have been updated!")
            # Here you would typically save these preferences to a database
            
    st.divider()
    
    # Learning style assessment
    st.subheader("Take a Learning Style Assessment")
    st.write("Not sure about your learning style? Take our quick assessment!")
    if st.button("Start Assessment"):
        st.info("Assessment feature coming soon!") 