# pages/admin_panel.py

import streamlit as st
from utils.database import Database

def admin_panel():
    """Admin Control Panel"""
    
    # Sidebar
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 20px 0;">
            <span style="font-size: 50px;">🛡️</span>
            <h3 style="margin: 10px 0; color: #667eea;">Admin Panel</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Stats in sidebar
        stats = Database.get_stats()
        st.markdown(f"""
        <div class="glass-card" style="padding: 15px;">
            <p style="color: #aaa; font-size: 11px; margin: 0;">SYSTEM OVERVIEW</p>
            <div style="margin-top: 10px;">
                <p style="margin: 5px 0; font-size: 13px;">👥 Total Users: <strong>{stats['total_users']}</strong></p>
                <p style="margin: 5px 0; font-size: 13px;">⏳ Pending: <strong style="color: #ffc107;">{stats['pending_users']}</strong></p>
                <p style="margin: 5px 0; font-size: 13px;">✅ Approved: <strong style="color: #28a745;">{stats['approved_users']}</strong></p>
                <p style="margin: 5px 0; font-size: 13px;">🎬 Videos: <strong>{stats['total_videos']}</strong></p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Logout
        if st.button("🚪 Logout", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    
    # Main Content
    st.markdown("""
    <div style="margin-bottom: 25px;">
        <h1>🛡️ Admin Control Panel</h1>
        <p style="color: #aaa;">Manage users, credits, and system settings</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Stats Row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Users", stats['total_users'])
    with col2:
        st.metric("Pending", stats['pending_users'], delta=None)
    with col3:
        st.metric("Approved", stats['approved_users'])
    with col4:
        st.metric("Total Videos", stats['total_videos'])
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Tabs
    tab1, tab2, tab3 = st.tabs(["⏳ Pending Approvals", "👥 All Users", "💰 Credit Management"])
    
    with tab1:
        show_pending_approvals()
    
    with tab2:
        show_all_users()
    
    with tab3:
        show_credit_management()

def show_pending_approvals():
    """Show pending user approvals"""
    st.markdown("### ⏳ Pending User Approvals")
    
    pending_users = Database.get_pending_users()
    
    if not pending_users:
        st.markdown("""
        <div class="glass-card" style="text-align: center; padding: 30px;">
            <span style="font-size: 40px;">✅</span>
            <h4>No Pending Users</h4>
            <p style="color: #aaa;">All users have been processed!</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    for email, data in pending_users.items():
        with st.expander(f"📧 {email} - Joined: {data['joined_date']}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"""
                <div style="padding: 10px;">
                    <p><strong>Email:</strong> {email}</p>
                    <p><strong>Joined:</strong> {data['joined_date']}</p>
                    <p><strong>Status:</strong> <span class="badge badge-pending">PENDING</span></p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("<br>", unsafe_allow_html=True)
                col_a, col_b = st.columns(2)
                with col_a:
                    if st.button("✅ Approve", key=f"approve_{email}", use_container_width=True):
                        Database.update_status(email, "approved")
                        st.success(f"User {email} approved!")
                        st.rerun()
                with col_b:
                    if st.button("❌ Reject", key=f"reject_{email}", use_container_width=True):
                        Database.update_status(email, "rejected")
                        st.warning(f"User {email} rejected!")
                        st.rerun()

def show_all_users():
    """Show all approved users"""
    st.markdown("### 👥 All Approved Users")
    
    approved_users = Database.get_approved_users()
    
    if not approved_users:
        st.info("No approved users yet!")
        return
    
    # Search
    search = st.text_input("🔍 Search users by email", placeholder="Type email...")
    
    for email, data in approved_users.items():
        if search and search.lower() not in email.lower():
            continue
        
        with st.expander(f"👤 {email} | 💰 {data['credits']} credits | 🎬 {len(data.get('videos_created', []))} videos"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"""
                <div style="padding: 10px;">
                    <p><strong>Email:</strong> {email}</p>
                    <p><strong>Joined:</strong> {data['joined_date']}</p>
                    <p><strong>Last Login:</strong> {data.get('last_login', 'Never')}</p>
                    <p><strong>Status:</strong> <span class="badge badge-approved">APPROVED</span></p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div style="padding: 10px;">
                    <p><strong>Credits:</strong> {data['credits']}</p>
                    <p><strong>Videos Created:</strong> {len(data.get('videos_created', []))}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                if st.button("🗑️ Remove User", key=f"remove_{email}", use_container_width=True):
                    Database.remove_user(email)
                    st.success(f"User {email} removed!")
                    st.rerun()

def show_credit_management():
    """Credit management section"""
    st.markdown("### 💰 Credit Management")
    
    st.markdown("""
    <div class="glass-card" style="margin-bottom: 20px;">
        <h4>💡 Quick Credit Add</h4>
        <p style="color: #aaa; font-size: 13px;">Add credits to any user account</p>
    </div>
    """, unsafe_allow_html=True)
    
    approved_users = Database.get_approved_users()
    
    if not approved_users:
        st.info("No approved users to manage credits!")
        return
    
    # Select user
    user_emails = list(approved_users.keys())
    selected_user = st.selectbox("👤 Select User", user_emails)
    
    if selected_user:
        user_data = approved_users[selected_user]
        current_credits = user_data['credits']
        
        st.markdown(f"""
        <div class="glass-card" style="text-align: center; padding: 20px;">
            <p style="color: #aaa;">Current Balance</p>
            <h2 style="color: #f6d365;">💰 {current_credits} Credits</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Add credits
        col1, col2 = st.columns([2, 1])
        with col1:
            credit_amount = st.number_input(
                "Amount to add",
                min_value=1,
                max_value=1000,
                value=10,
                step=5
            )
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("💎 Add Credits", use_container_width=True):
                success, new_balance = Database.add_credits(selected_user, credit_amount)
                if success:
                    st.success(f"Added {credit_amount} credits! New balance: {new_balance}")
                    st.balloons()
                    st.rerun()