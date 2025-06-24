import streamlit as st
import os
import tempfile
import zipfile
import requests
import json
from pathlib import Path
import mimetypes
import threading
from typing import Dict, List, Optional
import shutil
import re

# Configure page
st.set_page_config(
    page_title="CodeHarvest - Developer Tools",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark purple theme
st.markdown("""
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
""", unsafe_allow_html=True)

class CodeExtractor:
    def __init__(self):
        self.default_ignore_patterns = {
            'node_modules', '__pycache__', '.git', '.vscode', '.idea', 
            'dist', 'build', 'target', '.gradle', 'bin', 'obj',
            '.DS_Store', 'Thumbs.db', '*.pyc', '*.pyo', '*.class',
            '.env', '.env.local', '.env.production', 'venv', 'env',
            'coverage', '.nyc_output', '*.log', '*.tmp', '*.temp'
        }
        
        self.code_extensions = {
            '.py', '.js', '.jsx', '.ts', '.tsx', '.java', '.c', '.cpp', 
            '.h', '.hpp', '.cs', '.php', '.rb', '.go', '.rs', '.swift',
            '.kt', '.scala', '.clj', '.hs', '.ml', '.r', '.m', '.pl',
            '.sh', '.bat', '.ps1', '.html', '.htm', '.css', '.scss',
            '.sass', '.less', '.xml', '.json', '.yaml', '.yml', '.toml',
            '.ini', '.cfg', '.conf', '.sql', '.md', '.rst', '.txt',
            '.dart', '.vue', '.svelte', '.elm', '.ex', '.exs', '.erl'
        }

    def should_ignore_file(self, file_path: str, ignore_patterns: set) -> bool:
        file_name = os.path.basename(file_path)
        file_path_lower = file_path.lower()
        
        for pattern in ignore_patterns:
            pattern_lower = pattern.lower().strip()
            if pattern_lower in file_path_lower or pattern_lower == file_name.lower():
                return True
            if pattern_lower.startswith('*.') and file_name.lower().endswith(pattern_lower[1:]):
                return True
        
        return False

    def is_binary_file(self, file_path: str) -> bool:
        try:
            mime_type, _ = mimetypes.guess_type(file_path)
            if mime_type and mime_type.startswith('text'):
                return False
            
            with open(file_path, 'rb') as f:
                chunk = f.read(1024)
                if b'\0' in chunk:
                    return True
            return False
        except:
            return True

    def extract_from_folder(self, folder_path: str, max_size_kb: int = 500, 
                          include_binary: bool = False, custom_patterns: str = "") -> Dict:
        max_size_bytes = max_size_kb * 1024
        ignore_patterns = self.default_ignore_patterns.copy()
        
        if custom_patterns:
            ignore_patterns.update(p.strip() for p in custom_patterns.split(',') if p.strip())
        
        content = []
        content.append(f"# Project Code Extract: {os.path.basename(folder_path)}\n")
        content.append(f"# Source: {folder_path}\n")
        content.append(f"# Max file size: {max_size_kb}KB\n")
        content.append("="*80 + "\n\n")
        
        # Generate folder structure
        content.append("## FOLDER STRUCTURE\n")
        content.append("```\n\n")
        content.extend(self._generate_tree_structure(folder_path, ignore_patterns))
        content.append("```\n\n")
        
        # Extract file contents
        content.append("## FILE CONTENTS\n\n")
        
        file_count = 0
        skipped_files = []
        file_contents = {}
        
        for root, dirs, files in os.walk(folder_path):
            dirs[:] = [d for d in dirs if not self.should_ignore_file(os.path.join(root, d), ignore_patterns)]
            
            for file in files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, folder_path)
                
                if self.should_ignore_file(file_path, ignore_patterns):
                    continue
                
                try:
                    file_size = os.path.getsize(file_path)
                    if file_size > max_size_bytes:
                        skipped_files.append(f"{relative_path} (size: {file_size//1024}KB)")
                        continue
                except:
                    continue
                
                file_ext = os.path.splitext(file)[1].lower()
                is_binary = self.is_binary_file(file_path)
                
                if is_binary and not include_binary:
                    if file_ext not in self.code_extensions:
                        continue
                
                try:
                    content.append(f"### {relative_path}\n")
                    content.append("```")
                    
                    if is_binary:
                        file_content = "[Binary file - content not displayed]\n"
                    else:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            file_content = f.read()
                            if not file_content.endswith('\n'):
                                file_content += '\n'
                    
                    content.append(file_content)
                    content.append("```\n\n")
                    
                    # Store individual file content
                    file_contents[relative_path] = file_content
                    file_count += 1
                    
                except Exception as e:
                    skipped_files.append(f"{relative_path} (error: {str(e)})")
        
        if skipped_files:
            content.append("## SKIPPED FILES\n")
            content.append("The following files were skipped:\n")
            for skipped in skipped_files[:20]:
                content.append(f"- {skipped}\n")
            if len(skipped_files) > 20:
                content.append(f"... and {len(skipped_files) - 20} more files\n")
            content.append("\n")
        
        return {
            'content': "".join(content),
            'file_contents': file_contents,
            'file_count': file_count,
            'skipped_count': len(skipped_files)
        }

    def extract_from_github(self, repo_url: str, max_size_kb: int = 500, 
                          include_binary: bool = False, custom_patterns: str = "") -> Dict:
        # Parse GitHub URL
        if 'github.com' not in repo_url:
            raise ValueError("Invalid GitHub URL")
        
        # Extract owner and repo name
        parts = repo_url.rstrip('/').split('/')
        if len(parts) < 2:
            raise ValueError("Invalid GitHub URL format")
        
        owner = parts[-2]
        repo = parts[-1]
        
        # Download repository
        download_url = f"https://api.github.com/repos/{owner}/{repo}/zipball"
        
        with tempfile.TemporaryDirectory() as temp_dir:
            # Download zip file
            response = requests.get(download_url)
            response.raise_for_status()
            
            zip_path = os.path.join(temp_dir, "repo.zip")
            with open(zip_path, 'wb') as f:
                f.write(response.content)
            
            # Extract zip
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
            
            # Find extracted folder
            extracted_folders = [d for d in os.listdir(temp_dir) if os.path.isdir(os.path.join(temp_dir, d))]
            if not extracted_folders:
                raise ValueError("No folders found in downloaded repository")
            
            repo_folder = os.path.join(temp_dir, extracted_folders[0])
            
            # Extract code
            return self.extract_from_folder(repo_folder, max_size_kb, include_binary, custom_patterns)

    def _generate_tree_structure(self, folder_path: str, ignore_patterns: set, prefix: str = "", is_last: bool = True) -> List[str]:
        tree_lines = []
        
        try:
            items = sorted(os.listdir(folder_path))
            items = [item for item in items if not self.should_ignore_file(os.path.join(folder_path, item), ignore_patterns)]
            
            for i, item in enumerate(items):
                item_path = os.path.join(folder_path, item)
                is_last_item = (i == len(items) - 1)
                
                connector = "└── " if is_last_item else "├── "
                tree_lines.append(f"{prefix}{connector}{item}\n")
                
                if os.path.isdir(item_path):
                    extension = "    " if is_last_item else "│   "
                    tree_lines.extend(self._generate_tree_structure(
                        item_path, ignore_patterns, prefix + extension, is_last_item
                    ))
        except PermissionError:
            pass
        
        return tree_lines

class FileStructureGenerator:
    def __init__(self):
        self.prompt_template = """
Please create a project structure using this simple format:

PROJECT_STRUCTURE:
project_name
project_name/folder1
project_name/folder1/file1.py
project_name/folder1/file2.js
project_name/folder2
project_name/folder2/subfolder1
project_name/folder2/subfolder1/file3.html
project_name/README.md
project_name/package.json

RULES:
- List each folder and file on a separate line
- Use forward slashes (/) to separate paths
- Folders can be empty (no files inside)
- Files must have extensions
- Start all paths with the project name

Add this to your AI prompt: "Create a project structure for: [YOUR REQUEST HERE]"
"""

    def parse_project_structure(self, ai_response: str) -> List[str]:
        """Parse AI response to extract project structure paths"""
        lines = ai_response.split('\n')
        
        # Find PROJECT_STRUCTURE section
        structure_start = -1
        
        for i, line in enumerate(lines):
            if 'PROJECT_STRUCTURE:' in line.upper():
                structure_start = i + 1
                break
        
        if structure_start == -1:
            # If no section found, try to extract paths from entire response
            structure_lines = [line.strip() for line in lines if line.strip() and '/' in line]
        else:
            # Extract lines until empty line or end
            structure_lines = []
            for i in range(structure_start, len(lines)):
                line = lines[i].strip()
                if not line:
                    break
                if line and not line.startswith('#') and not line.startswith('-'):
                    structure_lines.append(line)
        
        # Clean and validate paths
        valid_paths = []
        for path in structure_lines:
            path = path.strip()
            if path and ('/' in path or '.' in path):
                # Remove any leading/trailing quotes or special characters
                path = path.strip('"\'`-* ')
                if path:
                    valid_paths.append(path)
        
        return valid_paths

    def create_project_structure(self, base_path: str, structure_paths: List[str]) -> Dict:
        """Create the actual folder structure and files"""
        created_files = []
        created_folders = []
        errors = []
        
        try:
            # Create base directory if it doesn't exist
            os.makedirs(base_path, exist_ok=True)
            
            for path in structure_paths:
                try:
                    # Build full path
                    full_path = os.path.join(base_path, path)
                    
                    # Check if it's a file (has extension) or folder
                    if '.' in os.path.basename(path) and not path.endswith('/'):
                        # It's a file
                        dir_path = os.path.dirname(full_path)
                        if dir_path:
                            os.makedirs(dir_path, exist_ok=True)
                        
                        # Create empty file
                        with open(full_path, 'w', encoding='utf-8') as f:
                            f.write(f"# {os.path.basename(path)}\n# TODO: Add content\n")
                        
                        created_files.append(full_path)
                    else:
                        # It's a folder
                        os.makedirs(full_path, exist_ok=True)
                        created_folders.append(full_path)
                
                except Exception as e:
                    errors.append(f"Error creating {path}: {str(e)}")
        
        except Exception as e:
            errors.append(f"General error: {str(e)}")
        
        return {
            'created_files': created_files,
            'created_folders': created_folders,
            'errors': errors
        }

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

def main():
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

    # Main content area
    if tool_choice == "CodeXtractR":
        st.markdown("## 🔍 CodeXtractR - Code Extraction Tool")
        
        # Create two columns
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### ⚙️ Configuration")
            
            # Source selection
            source_type = st.radio(
                "Select source:",
                ["Local Folder", "GitHub Repository"]
            )
            
            if source_type == "Local Folder":
                folder_path = st.text_input("📂 Folder Path:", placeholder="Enter local folder path")
            else:
                repo_url = st.text_input("🔗 GitHub Repository URL:", 
                                       placeholder="https://github.com/user/repo")
            
            # Settings
            st.markdown("### 🎛️ Settings")
            max_size = st.number_input("Max file size (KB):", min_value=1, max_value=5000, value=500)
            include_binary = st.checkbox("Include binary files")
            custom_patterns = st.text_input("Additional ignore patterns:", 
                                          placeholder="*.log, temp/, cache/")
            
            # Extract button
            if st.button("🚀 Extract Code", type="primary"):
                extractor = CodeExtractor()
                
                try:
                    with st.spinner("Extracting code..."):
                        if source_type == "Local Folder":
                            if not folder_path or not os.path.exists(folder_path):
                                st.error("Please provide a valid folder path!")
                            else:
                                result = extractor.extract_from_folder(
                                    folder_path, max_size, include_binary, custom_patterns
                                )
                                st.session_state['extraction_result'] = result
                                st.session_state['source_type'] = 'local'
                                st.success(f"✅ Extracted {result['file_count']} files!")
                        else:
                            if not repo_url:
                                st.error("Please provide a GitHub repository URL!")
                            else:
                                result = extractor.extract_from_github(
                                    repo_url, max_size, include_binary, custom_patterns
                                )
                                st.session_state['extraction_result'] = result
                                st.session_state['source_type'] = 'github'
                                st.success(f"✅ Extracted {result['file_count']} files from GitHub!")
                
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
        
        with col2:
            st.markdown("### 📋 Extraction Results")
            
            if 'extraction_result' in st.session_state:
                result = st.session_state['extraction_result']
                
                # Metrics
                col_a, col_b = st.columns(2)
                with col_a:
                    st.metric("Files Extracted", result['file_count'])
                with col_b:
                    st.metric("Files Skipped", result['skipped_count'])
                
                # File explorer
                if result['file_contents']:
                    st.markdown("#### 📁 File Explorer")
                    selected_file = st.selectbox(
                        "Select a file to view:",
                        [""] + list(result['file_contents'].keys())
                    )
                    
                    if selected_file:
                        st.markdown(f"**📄 {selected_file}**")
                        
                        # Copy button for selected file
                        col_copy1, col_copy2 = st.columns([3, 1])
                        with col_copy2:
                            if st.button("📋 Copy File", key="copy_file"):
                                st.text_area(
                                    "File content (select all and copy):",
                                    value=result['file_contents'][selected_file],
                                    height=100,
                                    key="file_copy_area"
                                )
                                st.success("✅ File content ready to copy!")
                        
                        # Fixed size viewer with scrolling
                        st.markdown(f"""
                        <div class="file-viewer">{result['file_contents'][selected_file]}</div>
                        """, unsafe_allow_html=True)
                
                # Action buttons
                st.markdown("#### 🔧 Actions")
                col_x, col_y, col_z = st.columns(3)
                
                with col_x:
                    if st.button("📋 Copy Entire Codebase"):
                        st.text_area(
                            "Complete codebase (select all and copy):",
                            value=result['content'],
                            height=200,
                            key="full_copy_area"
                        )
                        st.success("✅ Complete codebase ready to copy!")
                
                with col_y:
                    if st.button("👀 Show Full Content"):
                        st.markdown("**Full Extracted Content:**")
                        st.markdown(f"""
                        <div class="copy-content">{result['content']}</div>
                        """, unsafe_allow_html=True)
                
                with col_z:
                    st.download_button(
                        label="💾 Download as Text",
                        data=result['content'],
                        file_name="code_extract.txt",
                        mime="text/plain"
                    )

    elif tool_choice == "SimpliFile":
        st.markdown("## 📁 SimpliFile - Project Structure Generator")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📝 Step 1: Get Custom Prompt")
            
            generator = FileStructureGenerator()
            
            if st.button("📋 Generate Custom Prompt"):
                st.text_area(
                    "Copy this prompt and add your request at the end:",
                    value=generator.prompt_template,
                    height=250,
                    help="Copy this prompt, add your project requirements at the end, and paste it to any AI assistant."
                )
            
            st.markdown("### 🤖 Step 2: Paste Project Structure")
            ai_response = st.text_area(
                "Paste the project structure here:",
                height=200,
                placeholder="Paste the project structure from AI response here...\nExample:\nmy_project\nmy_project/src\nmy_project/src/main.py\nmy_project/README.md"
            )
            
            st.markdown("### 📂 Step 3: Choose Destination")
            base_folder = st.text_input(
                "Base folder path:",
                placeholder="Enter where to create the project structure"
            )
        
        with col2:
            st.markdown("### 🚀 Generate Project")
            
            if st.button("🏗️ Create Project Structure", type="primary"):
                if not ai_response.strip():
                    st.error("Please paste the project structure first!")
                elif not base_folder.strip():
                    st.error("Please specify the base folder path!")
                else:
                    try:
                        with st.spinner("Creating project structure..."):
                            # Parse project structure
                            structure_paths = generator.parse_project_structure(ai_response)
                            
                            if not structure_paths:
                                st.error("Could not find valid project structure in the response!")
                                st.info("Make sure your response contains paths like: project_name/folder/file.ext")
                            else:
                                # Create base folder if it doesn't exist
                                os.makedirs(base_folder, exist_ok=True)
                                
                                # Create structure
                                creation_result = generator.create_project_structure(
                                    base_folder, 
                                    structure_paths
                                )
                                
                                # Show results
                                if creation_result['errors']:
                                    st.warning("Some errors occurred:")
                                    for error in creation_result['errors']:
                                        st.error(f"❌ {error}")
                                
                                if creation_result['created_files'] or creation_result['created_folders']:
                                    st.success("✅ Project structure created successfully!")
                                    
                                    # Show metrics
                                    col_a, col_b = st.columns(2)
                                    with col_a:
                                        st.metric("Folders Created", len(creation_result['created_folders']))
                                    with col_b:
                                        st.metric("Files Created", len(creation_result['created_files']))
                                    
                                    # Show created items
                                    if creation_result['created_folders']:
                                        st.markdown("**📁 Created Folders:**")
                                        for folder in creation_result['created_folders'][:10]:
                                            st.text(f"📁 {os.path.relpath(folder, base_folder)}")
                                    
                                    if creation_result['created_files']:
                                        st.markdown("**📄 Created Files:**")
                                        for file in creation_result['created_files'][:10]:
                                            st.text(f"📄 {os.path.relpath(file, base_folder)}")
                                else:
                                    st.error("No files or folders were created!")
                    
                    except Exception as e:
                        st.error(f"❌ Error creating project structure: {str(e)}")
            
            # Preview section
            if ai_response.strip():
                try:
                    structure_paths = generator.parse_project_structure(ai_response)
                    if structure_paths:
                        st.markdown("### 👀 Preview")
                        st.markdown("**Detected Paths:**")
                        for path in structure_paths[:15]:
                            if '.' in os.path.basename(path):
                                st.text(f"📄 {path}")
                            else:
                                st.text(f"📁 {path}")
                        
                        if len(structure_paths) > 15:
                            st.text("... (truncated)")
                        
                        st.markdown(f"**Total items:** {len(structure_paths)}")
                    else:
                        st.warning("⚠️ No valid paths detected. Make sure your structure uses format like: project/folder/file.ext")
                
                except Exception as e:
                    st.warning(f"⚠️ Could not parse structure: {str(e)}")

if __name__ == "__main__":
    main()
