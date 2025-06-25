import streamlit as st
import os
from typing import Dict, List

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

followed by file content in same order

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

def render_simplifile():
    """Render the SimpliFile tool interface"""
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
