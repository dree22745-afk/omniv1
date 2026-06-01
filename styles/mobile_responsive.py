# styles/mobile_responsive.py

MOBILE_CSS = """
<style>
/* ========================================== */
/*        MOBILE RESPONSIVE STYLES            */
/* ========================================== */

/* Mobile Devices (up to 768px) */
@media screen and (max-width: 768px) {
    /* Container Full Width */
    .main .block-container {
        padding: 0.5rem !important;
        margin: 0 !important;
    }
    
    /* Bigger Touch Targets */
    .stButton > button {
        height: 50px !important;
        font-size: 18px !important;
        border-radius: 25px !important;
        margin: 5px 0 !important;
    }
    
    /* Form Inputs Full Width & Bigger */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        font-size: 16px !important;
        padding: 15px !important;
        border-radius: 12px !important;
    }
    
    /* Stack Columns Vertically */
    .row-widget.stHorizontal {
        flex-direction: column !important;
    }
    
    .row-widget.stHorizontal > div {
        width: 100% !important;
        margin: 5px 0 !important;
    }
    
    /* Full Width Cards */
    .glass-card {
        width: 100% !important;
        padding: 15px !important;
        margin: 10px 0 !important;
    }
    
    /* Responsive Typography */
    h1 {
        font-size: 22px !important;
        line-height: 1.2 !important;
    }
    
    h2 {
        font-size: 18px !important;
        line-height: 1.3 !important;
    }
    
    h3 {
        font-size: 16px !important;
        line-height: 1.4 !important;
    }
    
    p, span, div {
        font-size: 14px !important;
    }
    
    /* Tabs Scrollable on Mobile */
    .stTabs [data-baseweb="tab-list"] {
        overflow-x: auto !important;
        flex-wrap: nowrap !important;
        gap: 5px !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 8px 16px !important;
        font-size: 13px !important;
        white-space: nowrap !important;
    }
    
    /* Sidebar Full Width on Mobile */
    .css-1d391kg {
        width: 100% !important;
        min-width: 100% !important;
    }
    
    /* Expander Full Width */
    .streamlit-expanderHeader {
        padding: 10px 15px !important;
    }
    
    /* Metrics Smaller */
    [data-testid="stMetricValue"] {
        font-size: 1.8rem !important;
    }
    
    /* Contact Icons Wrap */
    .contact-icons-container {
        flex-direction: column !important;
        gap: 15px !important;
    }
    
    /* Video Cards Stack */
    .video-card {
        width: 100% !important;
    }
    
    /* Admin Table Scrollable */
    .admin-table-container {
        overflow-x: auto !important;
        -webkit-overflow-scrolling: touch !important;
    }
    
    /* Prevent Horizontal Scroll */
    body {
        overflow-x: hidden !important;
        position: relative !important;
    }
    
    /* Fix iframe videos */
    iframe {
        width: 100% !important;
        height: auto !important;
        aspect-ratio: 16/9 !important;
    }
    
    /* Select Box Bigger */
    .stSelectbox > div > div {
        font-size: 16px !important;
        padding: 5px !important;
    }
    
    /* Slider Touch Friendly */
    .stSlider > div {
        padding: 10px 0 !important;
    }
    
    /* Popup/Modal Full Screen */
    .popup-container {
        width: 95% !important;
        margin: 10px auto !important;
    }
}

/* Small Mobile Devices (up to 480px) */
@media screen and (max-width: 480px) {
    h1 { font-size: 20px !important; }
    h2 { font-size: 16px !important; }
    h3 { font-size: 14px !important; }
    
    .glass-card {
        padding: 12px !important;
    }
    
    .stButton > button {
        height: 45px !important;
        font-size: 16px !important;
    }
    
    .badge {
        font-size: 10px !important;
        padding: 3px 10px !important;
    }
}

/* Tablet Devices (769px to 1024px) */
@media screen and (min-width: 769px) and (max-width: 1024px) {
    .main .block-container {
        padding: 1rem !important;
    }
    
    h1 { font-size: 28px !important; }
    h2 { font-size: 22px !important; }
    h3 { font-size: 18px !important; }
    
    .stButton > button {
        height: 45px !important;
    }
}

/* Landscape Mode Fix */
@media screen and (max-width: 768px) and (orientation: landscape) {
    .main .block-container {
        padding: 0.5rem 1rem !important;
    }
    
    h1 { font-size: 20px !important; }
}

/* High DPI Screens */
@media (-webkit-min-device-pixel-ratio: 2), (min-resolution: 192dpi) {
    .glass-card {
        backdrop-filter: blur(20px) !important;
    }
}

/* Dark Mode Preference */
@media (prefers-color-scheme: dark) {
    .glass-card {
        background: rgba(255, 255, 255, 0.03) !important;
    }
}

/* Reduce Motion for Accessibility */
@media (prefers-reduced-motion: reduce) {
    * {
        animation-duration: 0.01ms !important;
        transition-duration: 0.01ms !important;
    }
}

/* Notch/Hole-punch Fix for iPhone */
@supports (padding: max(0px)) {
    .main .block-container {
        padding-left: max(1rem, env(safe-area-inset-left)) !important;
        padding-right: max(1rem, env(safe-area-inset-right)) !important;
    }
}

/* Fix Streamlit Specific Mobile Issues */
@media screen and (max-width: 768px) {
    /* Fix element spacing */
    .element-container {
        margin: 5px 0 !important;
    }
    
    /* Fix dataframes */
    .stDataFrame {
        font-size: 12px !important;
    }
    
    /* Fix charts */
    .stChart {
        max-width: 100% !important;
    }
    
    /* Fix code blocks */
    .stCodeBlock {
        font-size: 12px !important;
        overflow-x: auto !important;
    }
}
</style>
"""