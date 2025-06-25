import streamlit as st

def copy_to_clipboard(text: str) -> bool:
    """Copy text to clipboard using JavaScript"""
    try:
        # Use Streamlit's built-in clipboard functionality
        st.write(f"""
        <script>
        navigator.clipboard.writeText(`{text.replace('`', '\\`')}`).then(function() {{
            console.log('Text copied to clipboard');
        }});
        </script>
        """, unsafe_allow_html=True)
        return True
    except:
        return False

def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format"""
    if size_bytes == 0:
        return "0B"
    
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f}{size_names[i]}"

def validate_github_url(url: str) -> bool:
    """Validate if the URL is a valid GitHub repository URL"""
    return 'github.com' in url and len(url.rstrip('/').split('/')) >= 2
