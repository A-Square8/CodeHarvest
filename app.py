import streamlit as st
from config.settings import apply_custom_css, PAGE_CONFIG
from tools.codextractr import render_codextractr
from tools.simplifile import render_simplifile

def main():
    # Configure page
    st.set_page_config(**PAGE_CONFIG)
    
    # Apply custom styling
    apply_custom_css()
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🌾 CodeHarvest</h1>
        <p>Professional Developer Tools Suite</p>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar for tool selection
    with st.sidebar:
        st.markdown("### 🛠️ Developer Tools")
        
        tool_choice = st.selectbox(
            "Choose a tool:",
            ["CodeXtractR", "SimpliFile"],
            index=0
        )
        
        st.markdown("---")
        
        # Tool descriptions
        if tool_choice == "CodeXtractR":
            st.markdown("""
            <div class="tool-card">
                <div class="tool-title">🔍 CodeXtractR</div>
                <div class="tool-description">
                Extract and organize code from local projects or GitHub repositories. 
                Get a complete overview of your project structure with file contents, 
                perfect for documentation or AI analysis.
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        elif tool_choice == "SimpliFile":
            st.markdown("""
            <div class="tool-card">
                <div class="tool-title">📁 SimpliFile</div>
                <div class="tool-description">
                Generate project structures from AI descriptions. Get a simple prompt, 
                use it with any AI assistant, and automatically create the entire 
                folder structure.
                </div>
            </div>
            """, unsafe_allow_html=True)

    # Render selected tool
    if tool_choice == "CodeXtractR":
        render_codextractr()
    elif tool_choice == "SimpliFile":
        render_simplifile()

if __name__ == "__main__":
    main()
