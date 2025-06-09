import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import threading
from pathlib import Path
import mimetypes

class ProjectCodeExtractor:
    def __init__(self, root):
        self.root = root
        self.root.title("CodeHarvest - Project Code Extractor")
        self.root.geometry("1400x900")
        self.root.configure(bg='#1a1a1a')
        self.root.minsize(1000, 700)
        
        # Configure style for modern look
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Modern color scheme
        self.colors = {
            'bg_primary': '#1a1a1a',
            'bg_secondary': '#2d2d2d',
            'bg_tertiary': '#3d3d3d',
            'accent': '#0078d4',
            'accent_hover': '#106ebe',
            'success': '#16a085',
            'warning': '#f39c12',
            'text_primary': '#ffffff',
            'text_secondary': '#b0b0b0',
            'border': '#404040'
        }
        
        # Configure modern ttk styles
        self.configure_styles()
        
        self.selected_folder = ""
        self.extracted_content = ""
        
        # Default ignored patterns for different project types
        self.default_ignore_patterns = {
            'node_modules', '__pycache__', '.git', '.vscode', '.idea', 
            'dist', 'build', 'target', '.gradle', 'bin', 'obj',
            '.DS_Store', 'Thumbs.db', '*.pyc', '*.pyo', '*.class',
            '.env', '.env.local', '.env.production', 'venv', 'env',
            'coverage', '.nyc_output', '*.log', '*.tmp', '*.temp'
        }
        
        # Common code file extensions
        self.code_extensions = {
            '.py', '.js', '.jsx', '.ts', '.tsx', '.java', '.c', '.cpp', 
            '.h', '.hpp', '.cs', '.php', '.rb', '.go', '.rs', '.swift',
            '.kt', '.scala', '.clj', '.hs', '.ml', '.r', '.m', '.pl',
            '.sh', '.bat', '.ps1', '.html', '.htm', '.css', '.scss',
            '.sass', '.less', '.xml', '.json', '.yaml', '.yml', '.toml',
            '.ini', '.cfg', '.conf', '.sql', '.md', '.rst', '.txt',
            '.dart', '.vue', '.svelte', '.elm', '.ex', '.exs', '.erl'
        }
        
        self.setup_ui()
    
    def configure_styles(self):
        """Configure modern ttk styles"""
        # Configure ttk styles
        self.style.configure('Modern.TFrame', 
                           background=self.colors['bg_secondary'],
                           relief='flat',
                           borderwidth=1)
        
        self.style.configure('Card.TFrame',
                           background=self.colors['bg_secondary'],
                           relief='solid',
                           borderwidth=1)
        
        self.style.configure('Modern.TLabel', 
                           background=self.colors['bg_secondary'],
                           foreground=self.colors['text_primary'],
                           font=('Segoe UI', 10))
        
        self.style.configure('Title.TLabel',
                           background=self.colors['bg_primary'],
                           foreground=self.colors['text_primary'],
                           font=('Segoe UI', 24, 'bold'))
        
        self.style.configure('Subtitle.TLabel',
                           background=self.colors['bg_primary'],
                           foreground=self.colors['text_secondary'],
                           font=('Segoe UI', 11))
        
        self.style.configure('Modern.TEntry',
                           fieldbackground=self.colors['bg_tertiary'],
                           foreground=self.colors['text_primary'],
                           borderwidth=1,
                           insertcolor=self.colors['text_primary'],
                           font=('Segoe UI', 10))
        
        self.style.configure('Modern.TButton',
                           background=self.colors['bg_tertiary'],
                           foreground=self.colors['text_primary'],
                           borderwidth=1,
                           focuscolor='none',
                           font=('Segoe UI', 10))
        
        self.style.map('Modern.TButton',
                      background=[('active', self.colors['border']),
                                ('pressed', self.colors['bg_tertiary'])])
        
        self.style.configure('Modern.TLabelframe',
                           background=self.colors['bg_secondary'],
                           foreground=self.colors['text_primary'],
                           borderwidth=1,
                           relief='solid')
        
        self.style.configure('Modern.TLabelframe.Label',
                           background=self.colors['bg_secondary'],
                           foreground=self.colors['text_primary'],
                           font=('Segoe UI', 11, 'bold'))
        
        self.style.configure('Modern.TCheckbutton',
                           background=self.colors['bg_secondary'],
                           foreground=self.colors['text_primary'],
                           focuscolor='none',
                           font=('Segoe UI', 10))
    
    def create_modern_button(self, parent, text, command, style_type='primary', width=None):
        """Create a modern styled button"""
        if style_type == 'primary':
            bg_color = self.colors['accent']
            hover_color = self.colors['accent_hover']
        elif style_type == 'success':
            bg_color = self.colors['success']
            hover_color = '#138d75'
        elif style_type == 'warning':
            bg_color = self.colors['warning']
            hover_color = '#e67e22'
        else:
            bg_color = self.colors['bg_tertiary']
            hover_color = self.colors['border']
        
        btn = tk.Button(parent, text=text, command=command,
                       bg=bg_color, fg=self.colors['text_primary'],
                       font=('Segoe UI', 10, 'bold'),
                       relief='flat', borderwidth=0,
                       padx=20, pady=10,
                       cursor='hand2')
        
        if width:
            btn.configure(width=width)
        
        def on_enter(e):
            btn.configure(bg=hover_color)
        
        def on_leave(e):
            btn.configure(bg=bg_color)
        
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        
        return btn
    
    def setup_ui(self):
        # Main container with padding
        main_container = tk.Frame(self.root, bg=self.colors['bg_primary'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header section
        header_frame = tk.Frame(main_container, bg=self.colors['bg_primary'])
        header_frame.pack(fill=tk.X, pady=(0, 30))
        
        # Title and subtitle
        title_label = ttk.Label(header_frame, text="CodeHarvest", style='Title.TLabel')
        title_label.pack(anchor=tk.W)
        
        subtitle_label = ttk.Label(header_frame, text="Extract and organize your project code structure", 
                                  style='Subtitle.TLabel')
        subtitle_label.pack(anchor=tk.W, pady=(5, 0))
        
        # Main content area
        content_frame = tk.Frame(main_container, bg=self.colors['bg_primary'])
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left panel for controls
        left_panel = ttk.Frame(content_frame, style='Card.TFrame', padding=20)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left_panel.configure(width=400)
        left_panel.pack_propagate(False)
        
        # Folder selection section
        folder_section = ttk.LabelFrame(left_panel, text="Project Folder", 
                                       style='Modern.TLabelframe', padding=15)
        folder_section.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(folder_section, text="Select your project directory:", 
                 style='Modern.TLabel').pack(anchor=tk.W, pady=(0, 8))
        
        folder_input_frame = tk.Frame(folder_section, bg=self.colors['bg_secondary'])
        folder_input_frame.pack(fill=tk.X, pady=(0, 8))
        
        self.folder_entry = ttk.Entry(folder_input_frame, style='Modern.TEntry', font=('Segoe UI', 10))
        self.folder_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        browse_btn = self.create_modern_button(folder_input_frame, "Browse", self.browse_folder)
        browse_btn.pack(side=tk.RIGHT)
        
        # Settings section
        settings_section = ttk.LabelFrame(left_panel, text="Extraction Settings", 
                                         style='Modern.TLabelframe', padding=15)
        settings_section.pack(fill=tk.X, pady=(0, 20))
        
        # Max file size
        size_frame = tk.Frame(settings_section, bg=self.colors['bg_secondary'])
        size_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(size_frame, text="Max file size (KB):", style='Modern.TLabel').pack(side=tk.LEFT)
        self.max_size_var = tk.StringVar(value="500")
        size_entry = ttk.Entry(size_frame, textvariable=self.max_size_var, 
                              style='Modern.TEntry', width=8)
        size_entry.pack(side=tk.RIGHT)
        
        # Include binary files
        self.include_binary_var = tk.BooleanVar()
        binary_cb = ttk.Checkbutton(settings_section, text="Include binary files",
                                   variable=self.include_binary_var, style='Modern.TCheckbutton')
        binary_cb.pack(anchor=tk.W, pady=(0, 10))
        
        # Custom ignore patterns
        ttk.Label(settings_section, text="Additional ignore patterns:", 
                 style='Modern.TLabel').pack(anchor=tk.W, pady=(0, 5))
        self.ignore_patterns_var = tk.StringVar()
        ignore_entry = ttk.Entry(settings_section, textvariable=self.ignore_patterns_var,
                                style='Modern.TEntry')
        ignore_entry.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(settings_section, text="(comma-separated, e.g., *.log, temp/, cache/)",
                 style='Modern.TLabel').pack(anchor=tk.W)
        
        # Extract button
        extract_btn = self.create_modern_button(left_panel, "🚀 Extract Project Code", 
                                               self.extract_code, 'primary', 25)
        extract_btn.pack(pady=(20, 15))
        
        # Progress section
        progress_frame = tk.Frame(left_panel, bg=self.colors['bg_secondary'])
        progress_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.progress_var = tk.StringVar(value="Ready to extract")
        progress_label = ttk.Label(progress_frame, textvariable=self.progress_var, 
                                  style='Modern.TLabel')
        progress_label.pack(anchor=tk.W, pady=(0, 5))
        
        self.progress_bar = ttk.Progressbar(progress_frame, mode='indeterminate')
        self.progress_bar.pack(fill=tk.X)
        
        # Right panel for output
        right_panel = tk.Frame(content_frame, bg=self.colors['bg_secondary'], relief='solid', bd=1)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Output header
        output_header = tk.Frame(right_panel, bg=self.colors['bg_tertiary'], height=50)
        output_header.pack(fill=tk.X)
        output_header.pack_propagate(False)
        
        output_title = tk.Label(output_header, text="Extracted Code", 
                               bg=self.colors['bg_tertiary'], fg=self.colors['text_primary'],
                               font=('Segoe UI', 12, 'bold'))
        output_title.pack(side=tk.LEFT, padx=20, pady=15)
        
        # Action buttons frame (initially hidden)
        self.action_buttons_frame = tk.Frame(output_header, bg=self.colors['bg_tertiary'])
        self.action_buttons_frame.pack(side=tk.RIGHT, padx=20, pady=10)
        
        self.copy_btn = self.create_modern_button(self.action_buttons_frame, "📋 Copy", 
                                                 self.copy_to_clipboard, 'success')
        self.copy_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.export_btn = self.create_modern_button(self.action_buttons_frame, "💾 Export", 
                                                   self.export_to_file, 'warning')
        self.export_btn.pack(side=tk.LEFT)
        
        # Initially hide action buttons
        self.action_buttons_frame.pack_forget()
        
        # Output text area
        output_content = tk.Frame(right_panel, bg=self.colors['bg_secondary'])
        output_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        self.output_text = scrolledtext.ScrolledText(
            output_content, 
            wrap=tk.WORD,
            bg='#0d1117',
            fg='#e6edf3',
            insertbackground='#e6edf3',
            selectbackground='#264f78',
            selectforeground='#ffffff',
            font=('Consolas', 10),
            relief='flat',
            borderwidth=0
        )
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
        # Configure text tags for syntax highlighting
        self.output_text.tag_configure('header', foreground='#79c0ff', font=('Consolas', 11, 'bold'))
        self.output_text.tag_configure('filename', foreground='#ffa657', font=('Consolas', 10, 'bold'))
        self.output_text.tag_configure('structure', foreground='#7ee787')
        
        # Configure grid weights
        content_frame.grid_rowconfigure(0, weight=1)
        content_frame.grid_columnconfigure(1, weight=1)
    
    def browse_folder(self):
        folder_selected = filedialog.askdirectory(title="Select Project Folder")
        if folder_selected:
            self.selected_folder = folder_selected
            self.folder_entry.delete(0, tk.END)
            self.folder_entry.insert(0, folder_selected)
    
    def should_ignore_file(self, file_path, ignore_patterns):
        """Check if a file should be ignored based on patterns"""
        file_name = os.path.basename(file_path)
        file_path_lower = file_path.lower()
        
        for pattern in ignore_patterns:
            pattern_lower = pattern.lower().strip()
            if pattern_lower in file_path_lower or pattern_lower == file_name.lower():
                return True
            if pattern_lower.startswith('*.') and file_name.lower().endswith(pattern_lower[1:]):
                return True
        
        return False
    
    def is_binary_file(self, file_path):
        """Check if a file is binary"""
        try:
            mime_type, _ = mimetypes.guess_type(file_path)
            if mime_type and mime_type.startswith('text'):
                return False
            
            # Check first 1024 bytes for null characters
            with open(file_path, 'rb') as f:
                chunk = f.read(1024)
                if b'\0' in chunk:
                    return True
            return False
        except:
            return True
    
    def extract_code(self):
        if not self.selected_folder:
            messagebox.showerror("Error", "Please select a project folder first!")
            return
        
        if not os.path.exists(self.selected_folder):
            messagebox.showerror("Error", "Selected folder does not exist!")
            return
        
        # Hide action buttons during extraction
        self.action_buttons_frame.pack_forget()
        
        # Start extraction in a separate thread
        threading.Thread(target=self._extract_code_thread, daemon=True).start()
    
    def _extract_code_thread(self):
        try:
            self.progress_var.set("🔍 Analyzing project structure...")
            self.progress_bar.start()
            
            max_size_kb = int(self.max_size_var.get()) if self.max_size_var.get().isdigit() else 500
            max_size_bytes = max_size_kb * 1024
            
            # Combine default and custom ignore patterns
            ignore_patterns = self.default_ignore_patterns.copy()
            custom_patterns = self.ignore_patterns_var.get()
            if custom_patterns:
                ignore_patterns.update(p.strip() for p in custom_patterns.split(',') if p.strip())
            
            content = []
            content.append(f"# Project Code Extract: {os.path.basename(self.selected_folder)}\n")
            content.append(f"# Source: {self.selected_folder}\n")
            content.append(f"# Max file size: {max_size_kb}KB\n")
            content.append("="*80 + "\n\n")
            
            # Generate folder structure
            self.progress_var.set("📁 Building folder structure...")
            content.append("## FOLDER STRUCTURE\n")
            content.append("```\n")
            content.extend(self._generate_tree_structure(self.selected_folder, ignore_patterns))
            content.append("```\n\n")
            
            # Extract file contents
            self.progress_var.set("📄 Extracting file contents...")
            content.append("## FILE CONTENTS\n\n")
            
            file_count = 0
            skipped_files = []
            
            for root, dirs, files in os.walk(self.selected_folder):
                # Filter out ignored directories
                dirs[:] = [d for d in dirs if not self.should_ignore_file(os.path.join(root, d), ignore_patterns)]
                
                for file in files:
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, self.selected_folder)
                    
                    # Skip ignored files
                    if self.should_ignore_file(file_path, ignore_patterns):
                        continue
                    
                    # Check file size
                    try:
                        file_size = os.path.getsize(file_path)
                        if file_size > max_size_bytes:
                            skipped_files.append(f"{relative_path} (size: {file_size//1024}KB)")
                            continue
                    except:
                        continue
                    
                    # Check if it's a code file or if we should include binary files
                    file_ext = os.path.splitext(file)[1].lower()
                    is_binary = self.is_binary_file(file_path)
                    
                    if is_binary and not self.include_binary_var.get():
                        if file_ext not in self.code_extensions:
                            continue
                    
                    # Read and add file content
                    try:
                        content.append(f"### {relative_path}\n")
                        content.append("```" + (file_ext[1:] if file_ext else "") + "\n")
                        
                        if is_binary:
                            content.append("[Binary file - content not displayed]\n")
                        else:
                            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                file_content = f.read()
                                content.append(file_content)
                                if not file_content.endswith('\n'):
                                    content.append('\n')
                        
                        content.append("```\n\n")
                        file_count += 1
                        
                        # Update progress
                        self.progress_var.set(f"📄 Processed {file_count} files...")
                        
                    except Exception as e:
                        skipped_files.append(f"{relative_path} (error: {str(e)})")
            
            # Add summary
            if skipped_files:
                content.append("## SKIPPED FILES\n")
                content.append("The following files were skipped:\n")
                for skipped in skipped_files[:20]:  # Limit to first 20
                    content.append(f"- {skipped}\n")
                if len(skipped_files) > 20:
                    content.append(f"... and {len(skipped_files) - 20} more files\n")
                content.append("\n")
            
            self.extracted_content = "".join(content)
            
            # Update UI in main thread
            self.root.after(0, self._update_output)
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"An error occurred: {str(e)}"))
        finally:
            self.root.after(0, self._finish_extraction)
    
    def _generate_tree_structure(self, folder_path, ignore_patterns, prefix="", is_last=True):
        """Generate a tree structure of the folder"""
        tree_lines = []
        
        try:
            items = sorted(os.listdir(folder_path))
            # Filter out ignored items
            items = [item for item in items if not self.should_ignore_file(os.path.join(folder_path, item), ignore_patterns)]
            
            for i, item in enumerate(items):
                item_path = os.path.join(folder_path, item)
                is_last_item = (i == len(items) - 1)
                
                # Current item line
                connector = "└── " if is_last_item else "├── "
                tree_lines.append(f"{prefix}{connector}{item}\n")
                
                # If it's a directory, recurse
                if os.path.isdir(item_path):
                    extension = "    " if is_last_item else "│   "
                    tree_lines.extend(self._generate_tree_structure(
                        item_path, ignore_patterns, prefix + extension, is_last_item
                    ))
        except PermissionError:
            pass
        
        return tree_lines
    
    def _update_output(self):
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(1.0, self.extracted_content)
        
        # Show action buttons after successful extraction
        self.action_buttons_frame.pack(side=tk.RIGHT, padx=20, pady=10)
    
    def _finish_extraction(self):
        self.progress_bar.stop()
        self.progress_var.set("✅ Extraction completed successfully!")
    
    def copy_to_clipboard(self):
        if not self.extracted_content:
            messagebox.showwarning("Warning", "No content to copy!")
            return
        
        self.root.clipboard_clear()
        self.root.clipboard_append(self.extracted_content)
        
        # Show success feedback
        original_text = self.copy_btn.cget('text')
        self.copy_btn.configure(text="✅ Copied!")
        self.root.after(2000, lambda: self.copy_btn.configure(text=original_text))
    
    def export_to_file(self):
        if not self.extracted_content:
            messagebox.showwarning("Warning", "No content to export!")
            return
        
        # Default filename based on project name
        project_name = os.path.basename(self.selected_folder) if self.selected_folder else "project"
        default_filename = f"{project_name}_code_extract.txt"
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            initialfile=default_filename,
            filetypes=[("Text files", "*.txt"), ("Markdown files", "*.md"), ("All files", "*.*")]
        )
        
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(self.extracted_content)
                
                # Show success feedback
                original_text = self.export_btn.cget('text')
                self.export_btn.configure(text="✅ Exported!")
                self.root.after(2000, lambda: self.export_btn.configure(text=original_text))
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export file: {str(e)}")

def main():
    root = tk.Tk()
    app = ProjectCodeExtractor(root)
    root.mainloop()

if __name__ == "__main__":
    main()
