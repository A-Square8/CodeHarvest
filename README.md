🌾 CodeHarvest
A Modern Python GUI Tool for Project Code Extraction and Documentation
CodeHarvest simplifies project documentation by extracting your entire codebase structure and content into a single, organized document. Perfect for code reviews, documentation, AI assistance, and project sharing.

🚀 Features
✨ Smart Code Extraction

📁 Visual Folder Structure - Clean tree view of your project hierarchy
🔍 Intelligent Filtering - Automatically ignores build files, dependencies, and config files
📝 Multi-Language Support - Recognizes 40+ programming languages with syntax highlighting
⚡ Performance Optimized - Configurable file size limits and threaded processing

🎛️ Customizable Settings

📏 File Size Control - Set maximum file size limits (default: 500KB)
🚫 Custom Ignore Patterns - Add your own files/folders to ignore
🔧 Binary File Handling - Choose whether to include binary files
🎨 Modern Dark UI - Developer-friendly interface

📤 Multiple Export Options

📋 Copy to Clipboard - Instant sharing and pasting
💾 Export to File - Save as .txt or .md files
🏷️ Formatted Output - Clean markdown with syntax highlighting markers

📁 What Gets Extracted?
✅ Included by Default

All source code files (Python, JavaScript, Java, C++, etc.)
Configuration files (JSON, YAML, XML, etc.)
Documentation files (README, markdown, etc.)
Project structure and folder hierarchy
Small text-based files

❌ Automatically Ignored
node_modules/          # Node.js dependencies
__pycache__/          # Python cache
.git/                 # Git repository data
.vscode/              # VS Code settings
.idea/                # IntelliJ settings
dist/, build/         # Build outputs
venv/, env/           # Virtual environments
*.pyc, *.class        # Compiled files
.DS_Store             # System files
🌍 Supported Project Types
CategoryLanguages & FrameworksWeb DevelopmentHTML, CSS, JavaScript, TypeScript, React, Vue, Angular, SveltePythonPython scripts, Django, Flask, FastAPIMobileJava, Kotlin (Android), Swift (iOS), Dart (Flutter)DesktopC, C++, C#, Java, PythonBackendNode.js, PHP, Ruby, Go, Rust, ScalaData SciencePython, R, Jupyter notebooksDevOpsShell scripts, Docker, YAML configs
📋 Output Example
markdown# Project Code Extract: my-awesome-project
# Source: /path/to/my-awesome-project
# Max file size: 500KB
================================================================================

## FOLDER STRUCTURE
my-awesome-project/
├── src/
│   ├── components/
│   │   ├── Header.jsx
│   │   └── Footer.jsx
│   ├── utils/
│   │   └── helpers.js
│   └── App.js
├── public/
│   └── index.html
├── package.json
└── README.md

## FILE CONTENTS

### src/App.js
```javascript
import React from 'react';
import Header from './components/Header';

function App() {
  return (
    <div className="App">
      <Header />
      {/* Your app content */}
    </div>
  );
}

export default App;
package.json
json{
  "name": "my-awesome-project",
  "version": "1.0.0",
  "dependencies": {
    "react": "^18.0.0"
  }
}

## ⚙️ Advanced Configuration

### Custom Ignore Patterns
Add your own patterns in the "Additional Ignore Patterns" field:
*.log, temp/, cache/, *.tmp, secrets.json

### File Size Management
- Adjust the "Max File Size" setting to control which files get included
- Large files are automatically skipped and listed in the output
- Recommended: 100-1000KB depending on your project size

### Binary File Handling
Toggle "Include binary files" to:
- ✅ **Enabled**: Include binary files with placeholder text
- ❌ **Disabled**: Skip binary files entirely (recommended)

## 🎨 Use Cases

### 📚 **Documentation**
- Generate comprehensive project overviews
- Create code documentation for team members
- Prepare project handoffs

### 🤖 **AI Assistance**
- Feed entire codebase to AI tools like ChatGPT, Claude
- Get AI-powered code reviews and suggestions
- Enable AI to understand full project context

### 👥 **Code Reviews**
- Share complete project structure with reviewers
- Enable offline code review processes
- Create portable project snapshots

### 📖 **Learning & Teaching**
- Study open-source project structures
- Create educational code examples
- Analyze codebases for learning purposes

## 🔧 Customization

### Modify Default Ignore Patterns
Edit the `default_ignore_patterns` set in the code:
```python
self.default_ignore_patterns = {
    'node_modules', '__pycache__', '.git',
    'your_custom_folder', '*.your_extension'
}

Add New File Extensions
Extend the code_extensions set:
pythonself.code_extensions = {
    '.py', '.js', '.your_extension'
}

