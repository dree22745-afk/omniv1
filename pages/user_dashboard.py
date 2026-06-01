# pages/user_dashboard.py

import streamlit as st
import time
import os
from utils.database import Database
from utils.video_pipeline import VideoPipeline

def user_dashboard():
    """User Dashboard Page"""
    
    # Sidebar
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 20px 0;">
            <span style="font-size: 50px;">👤</span>
            <h3 style="margin: 10px 0; color: white;">Welcome!</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # User Info
        user_data = Database.get_user(st.session_state.user_email)
        if user_data:
            show_credit_bar(user_data['credits'])
            
            st.markdown(f"""
            <div class="glass-card" style="padding: 15px; margin: 15px 0;">
                <p style="color: #aaa; font-size: 12px; margin: 0;">📧 {st.session_state.user_email}</p>
                <p style="color: #aaa; font-size: 12px; margin: 5px 0 0 0;">📅 Joined: {user_data['joined_date']}</p>
                <p style="color: #aaa; font-size: 12px; margin: 5px 0 0 0;">🎬 Videos: {len(user_data.get('videos_created', []))}</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Logout Button
        if st.button("🚪 Logout", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    
    # Main Content
    tab1, tab2 = st.tabs(["🎬 Create Video", "📂 My Videos"])
    
    with tab1:
        show_video_creator()
    
    with tab2:
        show_video_history()

def show_credit_bar(credits):
    """Show credit balance"""
    st.markdown(f"""
    <div class="credit-display" style="text-align: center;">
        <p style="color: #aaa; font-size: 12px; margin: 0;">AVAILABLE CREDITS</p>
        <h2 class="credit-text" style="margin: 5px 0;">💰 {credits}</h2>
        <div style="display: flex; justify-content: space-around; font-size: 10px; color: #aaa; margin-top: 10px;">
            <span>📺 YT: 10</span>
            <span>📱 Reel: 5</span>
            <span>🎵 TT: 5</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def show_video_creator():
    """Video creation form with working pipeline"""
    
    st.markdown("""
    <div style="margin-bottom: 20px;">
        <h2>🎥 Create New Video</h2>
        <p style="color: #aaa; font-size: 14px;">Describe your video idea and let AI do the magic!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Command Input
    command = st.text_area(
        "💭 What video do you want to create?",
        height=120,
        placeholder="Example: Create a 30 second motivational video with dark cinematic style, slow motion effects, and epic background music. No text or captions needed.",
        help="Describe your video in detail - style, duration, effects, music preference etc."
    )
    
    # Options
    col1, col2, col3 = st.columns(3)
    with col1:
        platform = st.selectbox(
            "📱 Platform",
            ["YouTube", "Instagram Reel", "TikTok"],
            help="Select target platform for video dimensions"
        )
    with col2:
        duration = st.slider(
            "⏱️ Duration (seconds)",
            15, 120, 30, 5,
            help="Video duration in seconds"
        )
    with col3:
        voice = st.selectbox(
            "🎙️ Voice",
            ["adam", "antoni", "bella", "rachel"],
            help="Select voiceover narrator"
        )
    
    # Credit Cost Display
    credit_costs = {
        "YouTube": 10,
        "Instagram Reel": 5,
        "TikTok": 5
    }
    cost = credit_costs[platform]
    
    user_data = Database.get_user(st.session_state.user_email)
    current_credits = user_data['credits'] if user_data else 0
    
    st.markdown(f"""
    <div class="glass-card" style="padding: 10px 15px; margin: 15px 0; display: flex; justify-content: space-between; align-items: center;">
        <span style="color: #aaa; font-size: 13px;">💳 Video Cost:</span>
        <span style="font-weight: 600; color: {'#28a745' if current_credits >= cost else '#dc3545'};">
            {cost} Credits
        </span>
    </div>
    """, unsafe_allow_html=True)
    
    # Generate Button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        generate_btn = st.button(
            "🚀 Generate Video",
            use_container_width=True,
            disabled=current_credits < cost or not command
        )
    
    if current_credits < cost:
        st.warning(f"⚠️ Insufficient credits! You need {cost} credits. You have {current_credits}.")
    
    if generate_btn and command:
        # Progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # Initialize pipeline
            pipeline = VideoPipeline()
            
            # Step 1: Script
            status_text.info("📝 AI is writing your video script...")
            progress_bar.progress(10)
            
            # Step 2: Images
            status_text.info("🖼️ Generating scene images...")
            progress_bar.progress(30)
            
            # Step 3: Voiceover
            status_text.info("🎙️ Recording professional voiceover...")
            progress_bar.progress(60)
            
            # Step 4: Edit
            status_text.info("🎬 Editing video with effects...")
            progress_bar.progress(80)
            
            # Generate video
            success, message, video_path = pipeline.generate_video(
                st.session_state.user_email,
                command,
                platform,
                duration,
                "HD (1080p)",
                voice
            )
            
            progress_bar.progress(100)
            
            if success:
                status_text.success(f"✅ {message}")
                st.balloons()
                
                # Show video
                if video_path and os.path.exists(video_path):
                    st.video(video_path)
                    
                    # Download button
                    with open(video_path, 'rb') as f:
                        st.download_button(
                            "⬇️ Download Video",
                            f,
                            file_name=f"ai_video_{platform.lower().replace(' ', '_')}.mp4",
                            mime="video/mp4",
                            use_container_width=True
                        )
                
                # Refresh after 3 seconds
                time.sleep(3)
                st.rerun()
            else:
                status_text.error(f"❌ {message}")
                progress_bar.empty()
                
        except Exception as e:
            status_text.error(f"❌ Error: {str(e)}")
            progress_bar.empty()

def show_video_history():
    """Show user's video history"""
    st.markdown("""
    <div style="margin-bottom: 20px;">
        <h2>📂 My Videos</h2>
        <p style="color: #aaa; font-size: 14px;">Your previously created videos</p>
    </div>
    """, unsafe_allow_html=True)
    
    user_data = Database.get_user(st.session_state.user_email)
    
    if user_data and user_data.get('videos_created'):
        videos = user_data['videos_created']
        
        for i, video in enumerate(videos, 1):
            with st.expander(f"🎬 Video {i} - {video.get('created_at', 'Unknown Date')}"):
                st.markdown(f"""
                <div style="padding: 10px;">
                    <p><strong>Platform:</strong> {video.get('platform', 'N/A')}</p>
                    <p><strong>Duration:</strong> {video.get('duration', 'N/A')} seconds</p>
                    <p><strong>Command:</strong> {video.get('command', 'N/A')[:100]}...</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Placeholder for video player
                st.info("📹 Video preview will appear here")
    else:
        st.markdown("""
        <div class="glass-card" style="text-align: center; padding: 40px;">
            <span style="font-size: 60px;">📭</span>
            <h3>No Videos Yet</h3>
            <p style="color: #aaa;">Create your first video to see it here!</p>
        </div>
        """, unsafe_allow_html=True)