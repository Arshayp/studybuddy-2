if st.sidebar.button("Dashboard", use_container_width=True, key="nav_dashboard"):
    st.switch_page("dataanalystdashboard.py")
    
if st.sidebar.button("Student Matching", use_container_width=True, key="nav_matching"):
    st.switch_page("analyststudentmatching.py")
    
if st.sidebar.button("Retention Analysis", use_container_width=True, key="nav_retention"):
    st.switch_page("analystretention.py")
    
if st.sidebar.button("Geographic Data", use_container_width=True, key="nav_geographic"):
    st.switch_page("analystgeographic.py")
    
if st.sidebar.button("Academic Insights", use_container_width=True, key="nav_academic"):
    st.switch_page("analystacademic.py") 