import streamlit as st

# Page configuration
PAGE_CONFIG = {
    "page_title": "CodeHarvest - Developer Tools",
    "page_icon": "🌾",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# Custom CSS styles
CUSTOM_CSS = """
<style>
    .stApp {
        background: linear-gradient(135deg, #0d1117 0%, #161b22 100%);
    }
    
    .main-header {
        background: linear-gradient(90deg, #6f42c1, #8b5cf6);
        padding: 1rem 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 4px 20px rgba(111, 66, 193, 0.3);
    }
    
    .main-header h1 {
        color: white;
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
    }
    
    .main-header p {
        color: #e1e7ef;
        margin: 0.5rem 0 0 0;
        font-size: 1.1rem;
    }
    
    .tool-card {
        background: linear-gradient(145deg, #21262d, #30363d);
        border: 1px solid #6f42c1;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }
    
    .tool-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(111, 66, 193, 0.4);
        border-color: #8b5cf6;
    }
    
    .tool-title {
        color: #8b5cf6;
        font-size: 1.4rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .tool-description {
        color: #c9d1d9;
        font-size: 0.95rem;
        line-height: 1.5;
    }
    
    .stSelectbox > div > div {
        background-color: #21262d;
        border: 1px solid #6f42c1;
        border-radius: 8px;
    }
    
    .stTextInput > div > div > input {
        background-color: #0d1117;
        border: 1px solid #6f42c1;
        border-radius: 8px;
        color: #c9d1d9;
    }
    
    .stTextArea > div > div > textarea {
        background-color: #0d1117;
        border: 1px solid #6f42c1;
        border-radius: 8px;
        color: #c9d1d9;
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #6f42c1, #8b5cf6);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(90deg, #8b5cf6, #a855f7);
        transform: translateY(-1px);
        box-shadow: 0 4px 15px rgba(111, 66, 193, 0.4);
    }
    
    .file-viewer {
        background: #0d1117;
        border: 1px solid #30363d;
        border-radius: 8px;
        padding: 1rem;
        font-family: 'Courier New', monospace;
        color: #c9d1d9;
        height: 500px;
        overflow-y: auto;
        white-space: pre-wrap;
        font-size: 12px;
    }
    
    .copy-content {
        background: #0d1117;
        border: 1px solid #30363d;
        border-radius: 8px;
        padding: 1rem;
        font-family: 'Courier New', monospace;
        color: #c9d1d9;
        height: 400px;
        overflow-y: auto;
        white-space: pre-wrap;
        font-size: 11px;
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #161b22 0%, #0d1117 100%);
    }
    
    .metric-container {
        background: linear-gradient(145deg, #21262d, #30363d);
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        border: 1px solid #6f42c1;
    }
    
    .copy-button {
        background: linear-gradient(90deg, #28a745, #20c997);
        color: white;
        border: none;
        border-radius: 6px;
        padding: 0.4rem 1rem;
        font-weight: 500;
        font-size: 0.9rem;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .copy-button:hover {
        background: linear-gradient(90deg, #20c997, #17a2b8);
        transform: translateY(-1px);
    }
</style>
"""

def apply_custom_css():
    """Apply custom CSS styling to the Streamlit app"""
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
