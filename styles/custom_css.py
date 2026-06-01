# styles/custom_css.py

CUSTOM_CSS = """
<style>
/* Google Font Import */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');

/* Global Styles */
* {
    font-family: 'Poppins', sans-serif !important;
    margin: 0;
    padding: 0;
    box-sizing: border-box !important;
}

/* Body */
body {
    background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 100%) !important;
    color: white !important;
    overflow-x: hidden !important;
}

/* Hide Streamlit Default UI */
#MainMenu {visibility: hidden !important;}
footer {visibility: hidden !important;}
header {visibility: hidden !important;}

/* Main Container */
.main .block-container {
    padding: 1rem 2rem !important;
    max-width: 1200px !important;
    margin: 0 auto !important;
}

/* Custom Scrollbar */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

::-webkit-scrollbar-track {
    background: #1a1a2e;
    border-radius: 10px;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(135deg, #667eea, #764ba2);
    border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
    background: #764ba2;
}

/* Glass Morphism Effect */
.glass-card {
    background: rgba(255, 255, 255, 0.05) !important;
    backdrop-filter: blur(10px) !important;
    border-radius: 20px !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    padding: 25px !important;
    margin: 15px 0 !important;
    box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37) !important;
    transition: all 0.3s ease !important;
}

.glass-card:hover {
    border-color: rgba(102, 126, 234, 0.5) !important;
    box-shadow: 0 8px 32px 0 rgba(102, 126, 234, 0.3) !important;
}

/* Gradient Button */
.gradient-btn {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    color: white !important;
    border: none !important;
    padding: 12px 30px !important;
    border-radius: 25px !important;
    font-weight: 600 !important;
    font-size: 16px !important;
    cursor: pointer !important;
    transition: all 0.3s ease !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
}

.gradient-btn:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 10px 30px rgba(102, 126, 234, 0.5) !important;
}

/* Streamlit Button Override */
.stButton > button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    color: white !important;
    border: none !important;
    padding: 12px 30px !important;
    border-radius: 25px !important;
    font-weight: 600 !important;
    font-size: 16px !important;
    transition: all 0.3s ease !important;
    width: 100% !important;
}

.stButton > button:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 10px 30px rgba(102, 126, 234, 0.5) !important;
    border: none !important;
}

/* Input Fields */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: rgba(255, 255, 255, 0.05) !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    border-radius: 15px !important;
    color: white !important;
    padding: 12px 20px !important;
    font-size: 16px !important;
    transition: all 0.3s ease !important;
}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #667eea !important;
    box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.3) !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px !important;
    background: transparent !important;
}

.stTabs [data-baseweb="tab"] {
    background: rgba(255, 255, 255, 0.05) !important;
    border-radius: 12px 12px 0 0 !important;
    padding: 10px 24px !important;
    color: #aaa !important;
    font-weight: 500 !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #667eea, #764ba2) !important;
    color: white !important;
    border-color: transparent !important;
}

/* Expander */
.streamlit-expanderHeader {
    background: rgba(102, 126, 234, 0.1) !important;
    border-radius: 12px !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    font-weight: 600 !important;
}

/* Success/Error Messages */
.stSuccess {
    background: rgba(40, 167, 69, 0.15) !important;
    border: 1px solid rgba(40, 167, 69, 0.3) !important;
    border-radius: 12px !important;
    padding: 15px !important;
}

.stError {
    background: rgba(220, 53, 69, 0.15) !important;
    border: 1px solid rgba(220, 53, 69, 0.3) !important;
    border-radius: 12px !important;
    padding: 15px !important;
}

.stWarning {
    background: rgba(255, 193, 7, 0.15) !important;
    border: 1px solid rgba(255, 193, 7, 0.3) !important;
    border-radius: 12px !important;
    padding: 15px !important;
}

/* Metrics */
[data-testid="stMetricValue"] {
    font-size: 2.5rem !important;
    font-weight: 700 !important;
    background: linear-gradient(135deg, #667eea, #764ba2) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
}

/* Select Box */
.stSelectbox > div > div {
    background: rgba(255, 255, 255, 0.05) !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    border-radius: 15px !important;
}

/* Slider */
.stSlider > div > div > div > div {
    background: #667eea !important;
}

/* Sidebar */
.css-1d391kg, .css-1lcbmhc {
    background: rgba(10, 10, 10, 0.95) !important;
    backdrop-filter: blur(10px) !important;
}

/* Animations */
@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.fade-in-up {
    animation: fadeInUp 0.6s ease-out !important;
}

@keyframes pulse {
    0% { transform: scale(1); }
    50% { transform: scale(1.05); }
    100% { transform: scale(1); }
}

.pulse {
    animation: pulse 2s infinite !important;
}

/* Badges */
.badge {
    display: inline-block;
    padding: 5px 15px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
    margin: 5px;
}

.badge-pending {
    background: rgba(255, 193, 7, 0.2);
    color: #ffc107;
    border: 1px solid #ffc107;
}

.badge-approved {
    background: rgba(40, 167, 69, 0.2);
    color: #28a745;
    border: 1px solid #28a745;
}

.badge-rejected {
    background: rgba(220, 53, 69, 0.2);
    color: #dc3545;
    border: 1px solid #dc3545;
}

/* Credit Display */
.credit-display {
    background: linear-gradient(135deg, rgba(246, 211, 101, 0.1), rgba(253, 160, 133, 0.1));
    border: 1px solid rgba(246, 211, 101, 0.3);
    border-radius: 15px;
    padding: 15px 20px;
    margin: 10px 0;
}

.credit-text {
    background: linear-gradient(135deg, #f6d365, #fda085);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 700;
    font-size: 24px;
}
</style>
"""