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
## 💻 How to Install & Use the .exe (for Users)
Go to the Releases section of this GitHub repository.

Download the latest .zip file containing the .exe (Windows users only).

Unzip the file using tools like WinRAR or 7-Zip.

Double-click the .exe file to run CodeHarvest — no installation required.

If Windows shows a security warning:

Click "More info" > "Run anyway".

This happens because the .exe is not signed, but it's safe if downloaded from this repo.

⚠️ Note: The app requires Windows 10 or later. No need to install Python or other dependencies.
---

## 🛠️ Customization, Final Thoughts & Sharing the App

You can easily customize CodeHarvest and share it with others.

### 🔧 Ignore Patterns & File Types
To skip specific files or folders, and to add support for more file types, update the code like this:

```python
self.default_ignore_patterns = {
    'node_modules', '__pycache__', '.git',
    'your_custom_folder', '*.your_extension'
}

self.code_extensions = {
    '.py', '.js', '.your_extension'
}



🙌 Final Thoughts
CodeHarvest makes it simple to extract, document, and share your project code. Whether you're a developer preparing a handoff, a student submitting an assignment, or using AI tools to analyze code — this tool is made for you. It keeps your projects clean, readable, and ready to share


