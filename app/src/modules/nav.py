# naman
import streamlit as st


#### ------------------------ General ------------------------
def HomeNav():
    st.sidebar.page_link("Home.py", label="Home", icon="🏠")


def AboutPageNav():
    st.sidebar.page_link("pages/30_About.py", label="About", icon="🧠")


#### ------------------------ Examples for Role of pol_strat_advisor ------------------------
def PolStratAdvHomeNav():
    st.sidebar.page_link(
        "pages/00_Pol_Strat_Home.py", label="Political Strategist Home", icon="👤"
    )


def WorldBankVizNav():
    st.sidebar.page_link(
        "pages/01_World_Bank_Viz.py", label="World Bank Visualization", icon="🏦"
    )


def MapDemoNav():
    st.sidebar.page_link("pages/02_Map_Demo.py", label="Map Demonstration", icon="🗺️")


## ------------------------ Examples for Role of usaid_worker ------------------------
def ApiTestNav():
    st.sidebar.page_link("pages/12_API_Test.py", label="Test the API", icon="🛜")


def PredictionNav():
    st.sidebar.page_link(
        "pages/11_Prediction.py", label="Regression Prediction", icon="📈"
    )


def ClassificationNav():
    st.sidebar.page_link(
        "pages/13_Classification.py", label="Classification Demo", icon="🌺"
    )


#### ------------------------ System Admin Role ------------------------
def AdminPageNav():
    st.sidebar.page_link("pages/20_Admin_Home.py", label="System Admin", icon="🖥️")
    st.sidebar.page_link(
        "pages/21_ML_Model_Mgmt.py", label="ML Model Management", icon="🏢"
    )


# --------------------------------Links Function -----------------------------------------------
def SideBarLinks(show_home=False):
    """
    This function handles adding links to the sidebar of the app based upon the logged-in user's role, which was put in the streamlit session_state object when logging in.
    """

    # add a logo to the sidebar always
    st.sidebar.image("assets/logo.png", width=150)

    # If there is no logged in user, redirect to the Home (Landing) page
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.switch_page("Home.py")

    if show_home:
        # Show the Home page link (the landing page)
        HomeNav()

    # Show the other page navigators depending on the users' role.
    if st.session_state["authenticated"]:

        # Show World Bank Link and Map Demo Link if the user is a political strategy advisor role.
        if st.session_state["role"] == "pol_strat_advisor":
            PolStratAdvHomeNav()
            WorldBankVizNav()
            MapDemoNav()

        # If the user role is usaid worker, show the Api Testing page
        if st.session_state["role"] == "usaid_worker":
            PredictionNav()
            ApiTestNav()
            ClassificationNav()

        # If the user is an administrator, give them access to the administrator pages
        if st.session_state["role"] == "administrator":
            AdminPageNav()

    # Always show the About page at the bottom of the list of links
    AboutPageNav()

    if st.session_state["authenticated"]:
        # Always show a logout button if there is a logged in user
        if st.sidebar.button("Logout"):
            del st.session_state["role"]
            del st.session_state["authenticated"]
            st.switch_page("Home.py")

def nav_sidebar():
    """Draws the sidebar navigation links."""
    st.sidebar.image("assets/logo.png", width=150) # Display the logo
    st.sidebar.title("Navigation")
    
    # Show username if available
    user_name = st.session_state.get('user', {}).get('name', 'User')
    st.sidebar.write(f"Welcome, {user_name}")
    
    st.sidebar.divider()
    
    # Navigation Buttons
    if st.sidebar.button("Dashboard", use_container_width=True):
        st.switch_page("Home.py")
    
    if st.sidebar.button("Study Groups", use_container_width=True):
        st.switch_page("pages/study_groups.py")
    
    if st.sidebar.button("Find Partners", use_container_width=True):
        st.switch_page("pages/matching.py")
    
    if st.sidebar.button("Profile & Settings", use_container_width=True):
        st.switch_page("pages/profile.py")
    
    st.sidebar.divider()
    
    # Logout Button
    if st.sidebar.button("Logout", use_container_width=True):
        # Clear session state keys related to login
        for key in ['user', 'logged_in', 'preferences', 'settings']:
            if key in st.session_state:
                del st.session_state[key]
        # Ensure login state is reset
        st.session_state.logged_in = False
        st.session_state.page = 'login' 
        st.switch_page("pages/login.py")

def apply_basic_theme():
    """Hides default Streamlit footer and main menu."""
    hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

def setup_page(page_title):
    """Basic setup for authenticated pages: theme, sidebar, login check."""
    apply_basic_theme()
    
    # Check if user is logged in
    if not st.session_state.get('logged_in', False):
        st.warning("Please log in to access this page.")
        st.switch_page("pages/login.py")
        st.stop() # Stop execution if not logged in
    else:
        # If logged in, show the sidebar
        nav_sidebar()
