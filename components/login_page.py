# components/login_page.py

import streamlit as st
import time

def show_login_page():
    """Main Login/Signup Page"""
    
    # Header with Animation
    st.markdown("""
    <div style="text-align: center; padding: 30px 0 20px 0;" class="fade-in-up">
        <h1 style="font-size: 36px; margin-bottom: 5px;">
            <span style="background: linear-gradient(135deg, #667eea, #764ba2); 
                         -webkit-background-clip: text; 
                         -webkit-text-fill-color: transparent;">
                🎬 AI Video Editor Pro
            </span>
        </h1>
        <p style="color: #aaa; font-size: 16px; margin-top: 5px;">
            Professional Video Creation Suite
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Login Container
    st.markdown('<div class="glass-card fade-in-up" style="max-width: 450px; margin: 0 auto;">', unsafe_allow_html=True)
    
    # Tabs
    tab1, tab2 = st.tabs(["🔑 Login", "📝 Create Account"])
    
    with tab1:
        with st.form("login_form", clear_on_submit=False):
            email = st.text_input(
                "📧 Email Address",
                placeholder="your@email.com",
                key="login_email"
            )
            
            password = st.text_input(
                "🔒 Password",
                type="password",
                placeholder="••••••••",
                key="login_password"
            )
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                submit = st.form_submit_button(
                    "🚀 Login to Dashboard",
                    use_container_width=True
                )
            
            if submit:
                if not email or not password:
                    st.error("⚠️ Please fill all fields!")
                else:
                    return {
                        "action": "login",
                        "email": email.strip(),
                        "password": password
                    }
        
        # Forgot Password (Optional)
        st.markdown("""
        <p style="text-align: center; margin-top: 15px;">
            <span style="color: #666; font-size: 12px;">
                New user? Switch to <strong>Create Account</strong> tab
            </span>
        </p>
        """, unsafe_allow_html=True)
    
    with tab2:
        with st.form("signup_form", clear_on_submit=False):
            new_email = st.text_input(
                "📧 Email Address",
                placeholder="your@email.com",
                key="signup_email"
            )
            
            col1, col2 = st.columns(2)
            with col1:
                new_password = st.text_input(
                    "🔒 Password",
                    type="password",
                    placeholder="Min 6 characters",
                    key="signup_password"
                )
            with col2:
                confirm_password = st.text_input(
                    "🔒 Confirm Password",
                    type="password",
                    placeholder="Re-enter password",
                    key="signup_confirm"
                )
            
            # Terms
            st.markdown("""
            <p style="color: #666; font-size: 11px; text-align: center;">
                By creating account, you agree to our Terms of Service
            </p>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                submit = st.form_submit_button(
                    "✨ Create Free Account",
                    use_container_width=True
                )
            
            if submit:
                if not new_email or not new_password or not confirm_password:
                    st.error("⚠️ Please fill all fields!")
                elif "@" not in new_email or "." not in new_email:
                    st.error("⚠️ Please enter a valid email!")
                elif len(new_password) < 6:
                    st.error("⚠️ Password must be at least 6 characters!")
                elif new_password != confirm_password:
                    st.error("⚠️ Passwords do not match!")
                else:
                    return {
                        "action": "signup",
                        "email": new_email.strip(),
                        "password": new_password
                    }
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div style="text-align: center; margin-top: 30px; color: #666; font-size: 12px;" class="fade-in-up">
        <p>🔒 Secure Login • 256-bit Encryption</p>
        <p style="margin-top: 5px;">© 2026 AI Video Editor Pro. All rights reserved.</p>
    </div>
    """, unsafe_allow_html=True)
    
    return None