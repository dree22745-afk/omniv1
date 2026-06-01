# components/contact_popup.py

import streamlit as st

def show_contact_popup():
    """Show contact popup for pending users"""
    
    st.markdown("""
    <div class="glass-card fade-in-up" style="max-width: 500px; margin: 20px auto; text-align: center;">
        
        <!-- Header -->
        <div style="margin-bottom: 25px;">
            <span style="font-size: 60px;">⏳</span>
            <h2 style="background: linear-gradient(135deg, #ffc107, #ff9800); 
                       -webkit-background-clip: text; 
                       -webkit-text-fill-color: transparent;
                       margin: 10px 0;">
                Account Pending Approval
            </h2>
            <p style="color: #aaa; font-size: 14px; line-height: 1.6;">
                Your account is currently under review by our admin team.<br>
                <strong style="color: #ffc107;">Approval usually takes 2-4 hours.</strong>
            </p>
        </div>
        
        <!-- Divider -->
        <div style="height: 1px; background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent); margin: 20px 0;"></div>
        
        <!-- Contact Section -->
        <div style="margin: 25px 0;">
            <h3 style="color: white; margin-bottom: 15px;">📞 Need Immediate Access?</h3>
            <p style="color: #aaa; font-size: 13px; margin-bottom: 25px;">
                Contact us directly for instant approval:
            </p>
            
            <!-- Contact Icons -->
            <div style="display: flex; justify-content: center; gap: 20px; flex-wrap: wrap;">
                
                <!-- Instagram -->
                <a href="https://instagram.com/faizibhsi223" target="_blank" 
                   style="text-decoration: none; flex: 1; min-width: 100px;">
                    <div class="glass-card" style="padding: 20px 15px; cursor: pointer; text-align: center;">
                        <span style="font-size: 40px; display: block; margin-bottom: 10px;">📸</span>
                        <p style="background: linear-gradient(45deg, #f09433, #e6683c, #dc2743, #cc2366, #bc1888); 
                                  -webkit-background-clip: text; 
                                  -webkit-text-fill-color: transparent;
                                  font-weight: 600; font-size: 14px; margin: 5px 0;">
                            Instagram
                        </p>
                        <p style="color: #aaa; font-size: 11px; margin: 0;">@faizibhsi223</p>
                    </div>
                </a>
                
                <!-- WhatsApp -->
                <a href="https://wa.me/923162529100" target="_blank" 
                   style="text-decoration: none; flex: 1; min-width: 100px;">
                    <div class="glass-card" style="padding: 20px 15px; cursor: pointer; text-align: center;">
                        <span style="font-size: 40px; display: block; margin-bottom: 10px;">💬</span>
                        <p style="color: #25D366; font-weight: 600; font-size: 14px; margin: 5px 0;">
                            WhatsApp
                        </p>
                        <p style="color: #aaa; font-size: 11px; margin: 0;">+92 316 2529100</p>
                    </div>
                </a>
                
                <!-- Email -->
                <a href="mailto:faizibhai223@gmail.com" 
                   style="text-decoration: none; flex: 1; min-width: 100px;">
                    <div class="glass-card" style="padding: 20px 15px; cursor: pointer; text-align: center;">
                        <span style="font-size: 40px; display: block; margin-bottom: 10px;">📧</span>
                        <p style="color: #EA4335; font-weight: 600; font-size: 14px; margin: 5px 0;">
                            Email
                        </p>
                        <p style="color: #aaa; font-size: 11px; margin: 0;">faizibhai223@gmail.com</p>
                    </div>
                </a>
                
            </div>
        </div>
        
        <!-- Divider -->
        <div style="height: 1px; background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent); margin: 20px 0;"></div>
        
        <!-- Tip -->
        <div style="background: rgba(102, 126, 234, 0.1); padding: 15px; border-radius: 12px; border: 1px solid rgba(102, 126, 234, 0.2);">
            <p style="margin: 0; font-size: 13px; color: #aaa;">
                💡 <strong style="color: #667eea;">Pro Tip:</strong> WhatsApp pe message karo — sabse fast response milega!
            </p>
        </div>
        
        <!-- Refresh Button -->
        <div style="margin-top: 20px;">
            <p style="color: #666; font-size: 11px;">
                Already approved? Refresh the page or login again.
            </p>
        </div>
        
    </div>
    """, unsafe_allow_html=True)

def show_rejected_popup():
    """Show rejected message"""
    st.markdown("""
    <div class="glass-card fade-in-up" style="max-width: 500px; margin: 20px auto; text-align: center;">
        <span style="font-size: 60px;">❌</span>
        <h2 style="color: #dc3545; margin: 10px 0;">Account Rejected</h2>
        <p style="color: #aaa;">
            Your account has been rejected by the admin.<br>
            Please contact us for more information.
        </p>
    </div>
    """, unsafe_allow_html=True)