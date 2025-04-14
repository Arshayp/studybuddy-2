import streamlit as st
from datetime import datetime
from modules.nav import setup_page

# Page Configuration
st.set_page_config(
    page_title="StudyBuddy - Dashboard",
    page_icon="📊",
    layout="wide"
)

# Setup: Theme, Auth, Sidebar
setup_page("Admin Dashboard") 

st.title("StudyBuddy Admin Dashboard")
