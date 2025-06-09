# 🌾 CodeHarvest

**A Modern Python GUI Tool for Project Code Extraction and Documentation**

CodeHarvest simplifies project documentation by extracting your entire codebase structure and content into a single, organized document. Perfect for code reviews, documentation, AI assistance, and project sharing.

---

## 🚀 Features

### ✨ Smart Code Extraction
- 📁 **Visual Folder Structure** – Clean tree view of your project hierarchy  
- 🔍 **Intelligent Filtering** – Automatically ignores build files, dependencies, and config files  
- 📝 **Multi-Language Support** – Recognizes 40+ programming languages with syntax highlighting  
- ⚡ **Performance Optimized** – Configurable file size limits and threaded processing  

### 🎛️ Customizable Settings
- 📏 **File Size Control** – Set maximum file size limits (default: 500KB)  
- 🚫 **Custom Ignore Patterns** – Add your own files/folders to ignore  
- 🔧 **Binary File Handling** – Choose whether to include binary files  
- 🎨 **Modern Dark UI** – Developer-friendly interface  

### 📤 Multiple Export Options
- 📋 **Copy to Clipboard** – Instant sharing and pasting  
- 💾 **Export to File** – Save as `.txt` or `.md`  
- 🏷️ **Formatted Output** – Clean markdown with syntax highlighting markers  

---

## 📁 What Gets Extracted?

### ✅ Included by Default
- Source code files (`.py`, `.js`, `.java`, `.cpp`, etc.)
- Configuration files (`.json`, `.yml`, `.xml`, etc.)
- Documentation files (`README.md`, markdown, `.txt`, etc.)
- Project structure and folder hierarchy
- Small text-based files

### ❌ Automatically Ignored
node_modules/ # Node.js dependencies
pycache/ # Python cache
.git/ # Git repository data
.vscode/ # VS Code settings
.idea/ # IntelliJ settings
dist/, build/ # Build outputs
venv/, env/ # Virtual environments
*.pyc, *.class # Compiled files
.DS_Store # System files



### 📏 File Size Management
- Adjust the **Max File Size** setting to control which files get included  
- Large files are automatically skipped and listed in the output  
- **Recommended:** 100–1000KB depending on your project size  

### 🧩 Binary File Handling
Toggle **Include binary files** to:
- ✅ **Enabled** – Include binary files with placeholder text  
- ❌ **Disabled** – Skip binary files entirely (recommended)  

---

## 🎨 Use Cases

### 📚 Documentation
- Generate comprehensive project overviews  
- Create documentation for team collaboration and onboarding  
- Simplify project handoffs  

### 🤖 AI Assistance
- Feed entire codebases to AI tools like ChatGPT, Claude  
- Enable AI-powered code reviews and analysis  
- Improve code understanding and automation  

### 👥 Code Reviews
- Share structured code snapshots with collaborators  
- Support offline or asynchronous code review workflows  

### 📖 Learning & Teaching
- Study open-source structures and best practices  
- Build educational examples and tutorials  
- Analyze codebases for academic or self-learning  

---

## 🔧 Customization

### Modify Default Ignore Patterns
In the source code:
```python
self.default_ignore_patterns = {
    'node_modules', '__pycache__', '.git',
    'your_custom_folder', '*.your_extension'
}

## Add New File Extensions
### Extend supported file types:


self.code_extensions = {
    '.py', '.js', '.your_extension'
}



---

## 🙌 Final Thoughts

CodeHarvest is built to streamline the often-overlooked task of codebase documentation. Whether you're a developer preparing for a handoff, a student organizing project submissions, or an AI enthusiast feeding code into large language models — this tool is made for you. With its intuitive interface, powerful filtering, and flexible export options, CodeHarvest helps you focus less on formatting and more on what matters: your code. 🌱


