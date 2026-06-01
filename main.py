# main.py - MAIN APPLICATION ENTRY POINT

import streamlit as st
from styles.custom_css import CUSTOM_CSS
from styles.mobile_responsive import MOBILE_CSS
from utils.database import Database
from components.login_page import show_login_page
from components.contact_popup import show_contact_popup, show_rejected_popup
from pages.user_dashboard import user_dashboard
from pages.admin_panel import admin_panel

# ============================================
# PAGE CONFIGURATION
# ============================================
st.set_page_config(
    page_title="AI Video Editor Pro",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================
# INJECT CUSTOM CSS
# ============================================
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
st.markdown(MOBILE_CSS, unsafe_allow_html=True)

# ============================================
# SESSION STATE INITIALIZATION
# ============================================
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_role' not in st.session_state:
    st.session_state.user_role = None
if 'user_email' not in st.session_state:
    st.session_state.user_email = None
if 'login_error' not in st.session_state:
    st.session_state.login_error = None

# ============================================
# MAIN APP LOGIC
# ============================================
def main():
    """Main Application Router"""
    
    # If user is logged in
    if st.session_state.logged_in:
        if st.session_state.user_role == "admin":
            admin_panel()
        elif st.session_state.user_role == "user":
            user_dashboard()
        else:
            # Fallback - shouldn't happen
            st.error("Unknown role! Please login again.")
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    
    # If user is not logged in
    else:
        # Show login page and handle response
        login_response = show_login_page()
        
        if login_response:
            action = login_response['action']
            email = login_response['email']
            password = login_response['password']
            
            if action == "login":
                # Handle login
                role, message = Database.verify_login(email, password)
                
                if role == "admin":
                    st.session_state.logged_in = True
                    st.session_state.user_role = "admin"
                    st.session_state.user_email = email
                    st.success(message)
                    st.balloons()
                    st.rerun()
                
                elif role == "user":
                    st.session_state.logged_in = True
                    st.session_state.user_role = "user"
                    st.session_state.user_email = email
                    st.success(message)
                    st.balloons()
                    st.rerun()
                
                elif role == "pending":
                    st.warning(message)
                    show_contact_popup()
                
                elif role == "rejected":
                    st.error(message)
                    show_rejected_popup()
                
                else:
                    st.error(message)
            
            elif action == "signup":
                # Handle signup
                success, message = Database.create_user(email, password)
                
                if success:
                    st.success(message)
                    show_contact_popup()
                else:
                    st.error(message)

# ============================================
# RUN APP
# ============================================
if __name__ == "__main__":
    main()