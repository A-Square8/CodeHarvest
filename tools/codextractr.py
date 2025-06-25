import streamlit as st
import os
import tempfile
import zipfile
import requests
from pathlib import Path
import mimetypes
from typing import Dict, List

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

def render_codextractr():
    """Render the CodeXtractR tool interface"""
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
