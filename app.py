import tkinter as tk
from tkinter import filedialog, scrolledtext, ttk, messagebox
import os
import pyperclip
from pathlib import Path


class GoogleStyleFileCopyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Content Copier")
        self.root.geometry("1200x900")  # Increased window size
        self.root.minsize(1000, 800)  # Increased minimum size

        # Set theme colors - Google-inspired Material Design with more vibrant colors
        self.colors = {
            "bg_white": "#FFFFFF",
            "bg_light": "#F5F5F5",
            "bg_medium": "#EEEEEE",
            "accent": "#2979FF",  # Brighter blue
            "accent_light": "#D4E4FF",
            "accent_hover": "#0D47A1",
            "text_primary": "#202124",
            "text_secondary": "#5F6368",
            "success": "#00C853",  # Brighter green
            "warning": "#FFD600",  # Brighter yellow
            "error": "#FF3D00",  # Brighter red
            "border": "#DADCE0",
            "button_border": "#2979FF",  # Button outline color
        }

        # Configure style
        self.style = ttk.Style()
        self.style.theme_use("default")

        # Configure colors
        self.root.configure(bg=self.colors["bg_white"])

        # Configure styles for widgets
        self.configure_styles()

        self.setup_ui()

    def configure_styles(self):
        # Configure frame styles
        self.style.configure("TFrame", background=self.colors["bg_white"])
        self.style.configure(
            "Card.TFrame",
            background=self.colors["bg_white"],
            relief="solid",
            borderwidth=2,
            bordercolor=self.colors["border"],
        )

        # Configure label styles
        self.style.configure(
            "TLabel",
            background=self.colors["bg_white"],
            foreground=self.colors["text_primary"],
            font=("Helvetica", 12),
        )
        self.style.configure(
            "Header.TLabel",
            font=("Helvetica", 16, "bold"),
            foreground=self.colors["text_primary"],
        )
        self.style.configure(
            "Subheader.TLabel",
            font=("Helvetica", 14),
            foreground=self.colors["text_secondary"],
        )

        # Configure button styles
        self.style.configure(
            "TButton",
            background=self.colors["bg_white"],
            foreground=self.colors["accent"],
            font=("Helvetica", 12),
            relief="raised",
            borderwidth=2,
            padding=(15, 10),
        )
        self.style.map(
            "TButton",
            background=[("active", self.colors["accent_light"])],
            foreground=[("active", self.colors["accent_hover"])],
            relief=[("pressed", "sunken")],
        )

        # Primary button style
        self.style.configure(
            "Primary.TButton",
            background=self.colors["accent"],
            foreground="white",
            font=("Helvetica", 12, "bold"),
            relief="raised",
            borderwidth=2,
            padding=(20, 12),
        )
        self.style.map(
            "Primary.TButton",
            background=[("active", self.colors["accent_hover"])],
            foreground=[("active", "white")],
            relief=[("pressed", "sunken")],
        )

        # Configure entry styles - Bubbly and larger
        self.style.configure(
            "TEntry",
            fieldbackground=self.colors["bg_white"],
            foreground=self.colors["text_primary"],
            insertcolor=self.colors["text_primary"],
            borderwidth=2,
            relief="solid",
            padding=(10, 8),  # Add padding inside the entry field
        )

        # Configure checkbox styles - Larger and more visible
        self.style.configure(
            "TCheckbutton",
            background=self.colors["bg_white"],
            foreground=self.colors["text_primary"],
            font=("Helvetica", 12),  # Larger text
        )

        self.style.map(
            "TCheckbutton",
            background=[("active", self.colors["bg_white"])],
            indicatorcolor=[
                ("selected", self.colors["accent"]),
                ("!selected", self.colors["bg_medium"]),
            ],
            indicatorrelief=[("pressed", "sunken"), ("!pressed", "raised")],
        )

        # Configure treeview styles - More compact
        self.style.configure(
            "Treeview",
            background=self.colors["bg_white"],
            foreground=self.colors["text_primary"],
            fieldbackground=self.colors["bg_white"],
            font=("Helvetica", 11),  # Slightly smaller font
            rowheight=25,  # Reduced row height
            borderwidth=2,
            relief="solid",
        )
        self.style.configure(
            "Treeview.Heading",
            background=self.colors["bg_light"],
            foreground=self.colors["text_secondary"],
            font=("Helvetica", 11, "bold"),
            relief="raised",
            borderwidth=1,
        )
        self.style.map(
            "Treeview.Heading", background=[("active", self.colors["bg_medium"])]
        )
        self.style.map(
            "Treeview",
            background=[("selected", self.colors["accent_light"])],
            foreground=[("selected", self.colors["accent"])],
        )

        # Configure scrollbar styles
        self.style.configure(
            "Vertical.TScrollbar",
            background=self.colors["bg_white"],
            troughcolor=self.colors["bg_light"],
            arrowcolor=self.colors["text_secondary"],
            borderwidth=0,
        )

        # Configure labelframe styles - More bubbly with rounded appearance
        self.style.configure(
            "TLabelframe",
            background=self.colors["bg_white"],
            borderwidth=2,
            relief="solid",
            bordercolor=self.colors["border"],
        )
        self.style.configure(
            "TLabelframe.Label",
            background=self.colors["bg_white"],
            foreground=self.colors["text_primary"],
            font=("Helvetica", 14, "bold"),  # Larger text
            padding=(8, 2),
        )

    def setup_ui(self):
        # Create main frame to hold all content
        self.main_frame = ttk.Frame(self.root, padding="25")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Create rounded card containers with padding
        self.create_path_section(self.main_frame)
        self.create_options_section(self.main_frame)
        self.create_action_section(self.main_frame)
        self.create_file_selection_section(self.main_frame)
        self.create_preview_section(self.main_frame)

        # Status bar - Bubbly style
        status_frame = ttk.Frame(self.main_frame)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=(15, 0))  # Increased padding

        self.status_var = tk.StringVar()
        status_bar = ttk.Label(
            status_frame,
            textvariable=self.status_var,
            background=self.colors["accent_light"],
            foreground=self.colors["text_secondary"],
            padding=(20, 12),  # Larger padding
            relief="solid",
            borderwidth=1,
        )
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)

        # Store multiple file paths and data
        self.file_paths = []
        self.file_data = []
        self.file_positions = {}

    def create_path_section(self, parent):
        # Bubbly style heading
        path_heading = ttk.Label(
            parent, text="Select File or Directory", style="Header.TLabel"
        )
        path_heading.pack(anchor=tk.W, pady=(0, 10))  # Reduced padding

        path_frame = ttk.Frame(parent)
        path_frame.pack(fill=tk.X, pady=(0, 15))  # Reduced padding

        # Create a visual container for the input field with bubble styling
        entry_container = ttk.Frame(path_frame, style="Card.TFrame", padding=2)
        entry_container.pack(
            side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10)
        )  # Reduced padding

        self.path_var = tk.StringVar()
        path_entry = ttk.Entry(
            entry_container,
            textvariable=self.path_var,
            width=50,
            font=("Helvetica", 12),
        )
        path_entry.pack(fill=tk.BOTH, expand=True, ipady=6, padx=5)  # Reduced padding

        # Add some spacing between buttons
        button_frame = ttk.Frame(path_frame)
        button_frame.pack(side=tk.RIGHT)

        browse_file_btn = ttk.Button(
            button_frame,
            text="Browse Files",
            command=self.browse_file,
            style="TButton",
        )
        browse_file_btn.pack(side=tk.LEFT, padx=(0, 10))  # Reduced padding

        browse_dir_btn = ttk.Button(
            button_frame,
            text="Browse Directory",
            command=self.browse_directory,
            style="TButton",
        )
        browse_dir_btn.pack(side=tk.LEFT)

    def create_options_section(self, parent):
        # Bubbly style heading
        options_heading = ttk.Label(parent, text="Options", style="Header.TLabel")
        options_heading.pack(anchor=tk.W, pady=(0, 10))  # Reduced padding

        options_frame = ttk.Frame(
            parent, padding="15", style="Card.TFrame"
        )  # Reduced padding
        options_frame.pack(fill=tk.X, pady=(0, 15))  # Reduced padding

        # Modern grid layout with more spacing
        options_frame.columnconfigure(0, weight=1)
        options_frame.columnconfigure(1, weight=1)
        options_frame.columnconfigure(2, weight=1)

        # Directory options - Bubbly style checkboxes
        self.recursive_var = tk.BooleanVar(value=False)
        recursive_check = ttk.Checkbutton(
            options_frame, text="Include subdirectories", variable=self.recursive_var
        )
        recursive_check.grid(
            row=0, column=0, sticky=tk.W, padx=10, pady=8
        )  # Reduced padding

        self.show_paths_var = tk.BooleanVar(value=True)
        show_paths_check = ttk.Checkbutton(
            options_frame, text="Show file paths", variable=self.show_paths_var
        )
        show_paths_check.grid(
            row=1, column=0, sticky=tk.W, padx=10, pady=8
        )  # Reduced padding

        # File type ignore option
        ignore_label = ttk.Label(
            options_frame,
            text="Ignore file types:",
            foreground=self.colors["text_secondary"],
        )
        ignore_label.grid(
            row=2, column=0, sticky=tk.W, padx=10, pady=(8, 2)
        )  # Reduced padding

        # Bubbly styled entry
        self.ignore_types_var = tk.StringVar(value="")
        ignore_types_entry = ttk.Entry(
            options_frame,
            textvariable=self.ignore_types_var,
            width=30,
            font=("Helvetica", 12),
        )
        ignore_types_entry.grid(
            row=3,
            column=0,
            sticky=tk.W + tk.E,
            padx=10,
            pady=(0, 4),  # Reduced padding
        )

        info_label = ttk.Label(
            options_frame,
            text="(comma-separated extensions)",
            foreground=self.colors["text_secondary"],
            font=("Helvetica", 10),
        )
        info_label.grid(
            row=4, column=0, sticky=tk.W, padx=10, pady=(0, 8)
        )  # Reduced padding

        # Delimiter options with better alignment
        prefix_label = ttk.Label(
            options_frame,
            text="Prefix delimiter:",
            foreground=self.colors["text_secondary"],
        )
        prefix_label.grid(
            row=0, column=1, sticky=tk.E, padx=10, pady=8
        )  # Reduced padding

        self.prefix_delimiter_var = tk.StringVar(value="```")
        prefix_entry = ttk.Entry(
            options_frame,
            textvariable=self.prefix_delimiter_var,
            width=15,
            font=("Helvetica", 12),
        )
        prefix_entry.grid(
            row=0, column=2, padx=10, pady=8, sticky=tk.W
        )  # Reduced padding

        suffix_label = ttk.Label(
            options_frame,
            text="Suffix delimiter:",
            foreground=self.colors["text_secondary"],
        )
        suffix_label.grid(
            row=1, column=1, sticky=tk.E, padx=10, pady=8
        )  # Reduced padding

        self.suffix_delimiter_var = tk.StringVar(value="```")
        suffix_entry = ttk.Entry(
            options_frame,
            textvariable=self.suffix_delimiter_var,
            width=15,
            font=("Helvetica", 12),
        )
        suffix_entry.grid(
            row=1, column=2, padx=10, pady=8, sticky=tk.W
        )  # Reduced padding

    def create_action_section(self, parent):
        action_frame = ttk.Frame(parent)
        action_frame.pack(fill=tk.X, pady=(0, 15))  # Reduced padding

        self.process_btn = ttk.Button(
            action_frame,
            text="Process and Copy",
            command=self.process_path,
            style="Primary.TButton",
        )
        self.process_btn.pack(side=tk.LEFT, padx=(0, 15))  # Reduced padding

        clear_btn = ttk.Button(
            action_frame, text="Clear", command=self.clear_all, style="TButton"
        )
        clear_btn.pack(side=tk.LEFT)

    def create_file_selection_section(self, parent):
        # Bubbly style heading
        file_heading = ttk.Label(parent, text="File Selection", style="Header.TLabel")
        file_heading.pack(anchor=tk.W, pady=(0, 10))

        file_list_frame = ttk.Frame(parent, padding="15")
        file_list_frame.pack(fill=tk.X, pady=(0, 10))

        # Controls for file selection
        controls_frame = ttk.Frame(file_list_frame)
        controls_frame.pack(fill=tk.X, pady=(0, 10))

        select_all_btn = ttk.Button(
            controls_frame,
            text="Select All",
            command=self.select_all_files,
            style="TButton",
        )
        select_all_btn.pack(side=tk.LEFT, padx=(0, 10))

        deselect_all_btn = ttk.Button(
            controls_frame,
            text="Deselect All",
            command=self.deselect_all_files,
            style="TButton",
        )
        deselect_all_btn.pack(side=tk.LEFT)

        # File list with bubbly styling
        tree_frame = ttk.Frame(file_list_frame, style="Card.TFrame")
        tree_frame.pack(fill=tk.X, expand=True, pady=(10, 0), ipady=50)

        # Add scrollbar for file list
        file_list_scrollbar = ttk.Scrollbar(tree_frame, style="Vertical.TScrollbar")
        file_list_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Create treeview for file list with checkboxes - Hierarchical style
        self.file_tree = ttk.Treeview(
            tree_frame,
            columns=("checked", "path"),
            show="tree headings",
            selectmode="browse",
            yscrollcommand=file_list_scrollbar.set,
            style="Treeview",
            height=12,  # Increased number of visible rows
        )
        self.file_tree.heading("checked", text="Include")
        self.file_tree.heading("path", text="Path")
        self.file_tree.column("checked", width=60, anchor=tk.CENTER)
        self.file_tree.column("path", width=600)
        self.file_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        file_list_scrollbar.config(command=self.file_tree.yview)

        # Bind click event to toggle checkbox
        self.file_tree.bind("<ButtonRelease-1>", self.toggle_checkbox)

        # Bind click event for selection to scroll preview
        self.file_tree.bind("<<TreeviewSelect>>", self.scroll_to_file_in_preview)

        # Store directory structure
        self.directory_structure = {}

    def create_preview_section(self, parent):
        # Bubbly style heading
        preview_heading = ttk.Label(parent, text="Preview", style="Header.TLabel")
        preview_heading.pack(anchor=tk.W, pady=(0, 10))  # Reduced padding

        preview_frame = ttk.Frame(parent, padding="15")  # Reduced padding
        preview_frame.pack(fill=tk.X, pady=(0, 10))  # Reduced padding

        # Custom styled preview text - bubbly with clear borders
        preview_container = ttk.Frame(preview_frame, style="Card.TFrame", padding=2)
        preview_container.pack(fill=tk.X, expand=True)

        self.preview_text = scrolledtext.ScrolledText(
            preview_container,
            wrap=tk.WORD,
            height=8,  # Reduced height
            bg=self.colors["bg_white"],
            fg=self.colors["text_primary"],
            insertbackground=self.colors["text_primary"],
            selectbackground=self.colors["accent_light"],
            selectforeground=self.colors["accent"],
            borderwidth=0,
            font=("Courier", 12),
            padx=10,
            pady=10,
        )
        self.preview_text.pack(fill=tk.X, expand=True)

        # Configure tags for syntax highlighting - Bubbly colors
        self.preview_text.tag_configure(
            "highlight", background=self.colors["accent_light"]
        )
        self.preview_text.tag_configure(
            "file_path",
            foreground=self.colors["accent"],
            font=("Courier", 12, "bold"),
        )
        self.preview_text.tag_configure(
            "delimiter",
            foreground=self.colors["success"],
            font=("Courier", 12),
        )
        self.highlight_tag_configured = True

    def toggle_checkbox(self, event):
        item = self.file_tree.identify_row(event.y)
        column = self.file_tree.identify_column(event.x)

        if not item or column != "#1":  # First column is checkbox
            return

        current_value = self.file_tree.item(item, "values")[0]
        # Use more visible, bubbly checkbox indicators
        new_value = "☐" if current_value == "☑" else "☑"
        values = list(self.file_tree.item(item, "values"))
        values[0] = new_value
        self.file_tree.item(item, values=values)

        # If it's a directory, update all children
        if self.file_tree.get_children(item):

            def update_children(parent_item):
                for child in self.file_tree.get_children(parent_item):
                    child_values = list(self.file_tree.item(child, "values"))
                    child_values[0] = new_value
                    self.file_tree.item(child, values=child_values)
                    update_children(child)

            update_children(item)

        # Highlight the selected row for better visibility
        self.file_tree.selection_set(item)

    def scroll_to_file_in_preview(self, event):
        """Scroll the preview to the selected file's content."""
        # Get selected item
        selected_items = self.file_tree.selection()
        if not selected_items or not self.preview_text.get(1.0, tk.END).strip():
            return

        selected_item = selected_items[0]
        file_path = self.file_tree.item(selected_item, "values")[1]

        # Search for the file path in the preview
        preview_content = self.preview_text.get(1.0, tk.END)
        show_file_paths = self.show_paths_var.get()

        if not show_file_paths:
            # If file paths aren't shown, we can't easily find the right position
            messagebox.showinfo(
                "Info",
                "Enable 'Show file paths' option to use this feature",
                icon="info",
            )
            return

        # Find the position of the file path in the preview text
        start_pos = preview_content.find(file_path)
        if start_pos != -1:
            # Convert character position to line number
            line_number = preview_content[:start_pos].count("\n") + 1

            # Scroll to the line
            self.preview_text.see(f"{line_number}.0")

            # Highlight the section
            # Find the end of this file's section
            prefix_delimiter = self.prefix_delimiter_var.get()
            suffix_delimiter = self.suffix_delimiter_var.get()
            next_file_start = preview_content.find(
                file_path, start_pos + len(file_path)
            )

            if next_file_start == -1:
                end_pos = len(preview_content)
            else:
                end_pos = next_file_start - 1

            # Clear any existing tags
            self.preview_text.tag_remove("highlight", "1.0", tk.END)

            # Calculate positions for highlighting
            start_line = line_number
            end_line = preview_content[:end_pos].count("\n") + 1

            # Add highlighting tag
            self.preview_text.tag_add("highlight", f"{start_line}.0", f"{end_line}.0")

    def select_all_files(self):
        for item in self.file_tree.get_children():
            values = list(self.file_tree.item(item, "values"))
            values[0] = "☑"
            self.file_tree.item(item, values=values)

    def deselect_all_files(self):
        for item in self.file_tree.get_children():
            values = list(self.file_tree.item(item, "values"))
            values[0] = "☐"
            self.file_tree.item(item, values=values)

    def browse_file(self):
        file_paths = filedialog.askopenfilenames(title="Select file(s)")
        if file_paths:
            self.file_paths = file_paths
            if len(file_paths) == 1:
                self.path_var.set(file_paths[0])
            else:
                self.path_var.set(f"Selected {len(file_paths)} files")

    def browse_directory(self):
        dir_path = filedialog.askdirectory(title="Select a directory")
        if dir_path:
            self.file_paths = []  # Clear any selected files
            self.path_var.set(dir_path)

    def read_file(self, file_path):
        """Read and return the contents of a file."""
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return file.read()
        except UnicodeDecodeError:
            try:
                # Try reading as binary if utf-8 fails
                with open(file_path, "rb") as file:
                    binary_content = file.read()
                    return f"[Binary content - {len(binary_content)} bytes]"
            except Exception as e:
                return f"Error reading file: {str(e)}"
        except Exception as e:
            return f"Error reading file: {str(e)}"

    def should_ignore_file(self, file_path):
        """Check if a file should be ignored based on its name or extension."""
        file_name = os.path.basename(file_path)

        # Always ignore .DS_Store and .env files
        if file_name in [".DS_Store", ".env", ".env.local"]:
            return True

        # Get extensions to ignore from user input
        ignore_extensions = [
            ext.strip() for ext in self.ignore_types_var.get().split(",") if ext.strip()
        ]

        # Check if the file's extension should be ignored
        file_ext = os.path.splitext(file_name)[1].lower()
        for ext in ignore_extensions:
            # Ensure the extension starts with a dot
            if not ext.startswith("."):
                ext = "." + ext
            if file_ext == ext.lower():
                return True

        return False

    def select_directory(self):
        """Select or deselect all files in the currently selected directory."""
        selected_items = self.file_tree.selection()
        if not selected_items:
            messagebox.showinfo("Info", "Please select a directory first", icon="info")
            return

        selected_item = selected_items[0]
        item_values = self.file_tree.item(selected_item, "values")

        # Get current state of the directory checkbox
        current_state = item_values[0]
        new_state = "☐" if current_state == "☑" else "☑"

        # Update the selected directory
        values = list(item_values)
        values[0] = new_state
        self.file_tree.item(selected_item, values=values)

        # Update all child items (files and subdirectories)
        def update_children(item):
            for child in self.file_tree.get_children(item):
                child_values = list(self.file_tree.item(child, "values"))
                child_values[0] = new_state
                self.file_tree.item(child, values=child_values)
                update_children(child)

        update_children(selected_item)

    def process_directory(self, directory_path):
        """Process all files in a directory and return their contents."""
        files_to_process = []
        self.directory_structure = {}  # Reset directory structure

        if self.recursive_var.get():
            for root, dirs, files in os.walk(directory_path):
                # Skip __pycache__ directories
                if "__pycache__" in dirs:
                    dirs.remove("__pycache__")

                # Skip other common directories to ignore
                for ignore_dir in [
                    ".git",
                    ".hcl",
                    ".zip",
                    ".svn",
                    ".hg",
                    "__pycache__",
                    "node_modules",
                ]:
                    if ignore_dir in dirs:
                        dirs.remove(ignore_dir)

                # Add directories to the structure
                for dir_name in dirs:
                    dir_path = os.path.join(root, dir_name)
                    self.directory_structure[dir_path] = {
                        "type": "Directory",
                        "parent": root,
                    }

                for file in files:
                    file_path = os.path.join(root, file)
                    if not self.should_ignore_file(file_path):
                        files_to_process.append(file_path)
                        self.directory_structure[file_path] = {
                            "type": "File",
                            "parent": root,
                        }
        else:
            for item in os.listdir(directory_path):
                # Skip __pycache__ directories
                if item == "__pycache__":
                    continue

                item_path = os.path.join(directory_path, item)
                if os.path.isdir(item_path):
                    self.directory_structure[item_path] = {
                        "type": "Directory",
                        "parent": directory_path,
                    }
                elif os.path.isfile(item_path) and not self.should_ignore_file(
                    item_path
                ):
                    files_to_process.append(item_path)
                    self.directory_structure[item_path] = {
                        "type": "File",
                        "parent": directory_path,
                    }

        return files_to_process

    def get_files_to_scan(self):
        """Get the list of files to scan based on user selection."""
        path = self.path_var.get().strip()

        if not path and not self.file_paths:
            messagebox.showerror(
                "Error", "Please enter or select a file/directory path", icon="error"
            )
            return []

        # Check if we have multiple files selected
        if self.file_paths and len(self.file_paths) > 1:
            # Process multiple files
            return self.file_paths
        else:
            # Single file or directory path
            if path.startswith("Selected ") and " files" in path:
                # We have multiple files but need to use the stored paths
                return self.file_paths
            else:
                # Regular single path processing
                if not os.path.exists(path):
                    messagebox.showerror("Error", "Path does not exist", icon="error")
                    return []
                if os.path.isdir(path):
                    return self.process_directory(path)
                else:
                    return [path]

    def process_path(self):
        """Process path and handle files based on whether files have been scanned already."""
        # Check if we have already scanned files (file_data is populated)
        if self.file_data:
            self.process_selected_files()
        else:
            self.scan_and_process_files()

    def scan_and_process_files(self):
        """Scan the files, populate the file list, and copy all files in one go."""
        path = self.path_var.get().strip()

        if not path and not self.file_paths:
            messagebox.showerror(
                "Error", "Please enter or select a file/directory path", icon="error"
            )
            return

        # Clear existing file list
        for item in self.file_tree.get_children():
            self.file_tree.delete(item)

        # Get files to scan
        files_to_scan = self.get_files_to_scan()

        if not files_to_scan:
            return

        # Clear file data
        self.file_data = []
        errors = []

        # Create a mapping of paths to tree items
        path_to_item = {}

        # First, add directories to the tree
        for dir_path, info in self.directory_structure.items():
            if info["type"] == "Directory":
                parent = info["parent"]
                if parent == path:  # Root directory
                    item = self.file_tree.insert(
                        "",
                        "end",
                        text=os.path.basename(dir_path),
                        values=["☑", dir_path],
                    )
                else:
                    parent_item = path_to_item.get(parent)
                    if parent_item:
                        item = self.file_tree.insert(
                            parent_item,
                            "end",
                            text=os.path.basename(dir_path),
                            values=["☑", dir_path],
                        )
                    else:
                        item = self.file_tree.insert(
                            "",
                            "end",
                            text=os.path.basename(dir_path),
                            values=["☑", dir_path],
                        )
                path_to_item[dir_path] = item

        # Then process all files
        for file_path in files_to_scan:
            if not self.should_ignore_file(file_path):
                try:
                    # Read file content
                    content = self.read_file(file_path)
                    # Add to file data
                    self.file_data.append((file_path, content))

                    # Add to treeview with checkbox
                    parent = self.directory_structure[file_path]["parent"]
                    parent_item = path_to_item.get(parent)
                    if parent_item:
                        self.file_tree.insert(
                            parent_item,
                            "end",
                            text=os.path.basename(file_path),
                            values=["☑", file_path],
                        )
                    else:
                        self.file_tree.insert(
                            "",
                            "end",
                            text=os.path.basename(file_path),
                            values=["☑", file_path],
                        )
                except Exception as e:
                    errors.append((file_path, str(e)))

        if not self.file_data:
            if errors:
                error_msg = "No files were processed. Errors:\n"
                for file_path, error in errors:
                    error_msg += f"\n{file_path}: {error}"
                messagebox.showerror("Error", error_msg, icon="error")
            else:
                messagebox.showinfo("Info", "No files found to process", icon="info")
            return

        # Copy all files to clipboard on first run
        self.process_all_files()

        # Update status and button text
        self.status_var.set(
            f"✓ Copied {len(self.file_data)} files to clipboard. Uncheck files you don't want and click again to reprocess."
        )
        self.process_btn.config(text="Reprocess Selected Files")

        if errors:
            error_msg = "Some files could not be processed:\n"
            for file_path, error in errors:
                error_msg += f"\n{file_path}: {error}"
            messagebox.showwarning("Warnings", error_msg, icon="warning")

    def process_all_files(self):
        """Process all scanned files and copy to clipboard."""
        prefix_delimiter = self.prefix_delimiter_var.get()
        suffix_delimiter = self.suffix_delimiter_var.get()
        show_file_paths = self.show_paths_var.get()

        self.preview_text.delete(1.0, tk.END)

        try:
            all_content = ""
            # Store positions for each file in the preview for navigation
            self.file_positions = {}
            current_position = 0

            # Filter out directories from file_data
            actual_files = [
                (path, content)
                for path, content in self.file_data
                if os.path.isfile(path)
            ]

            for file_path, content in actual_files:
                # Store the starting position of this file in the preview
                self.file_positions[file_path] = current_position

                # Insert with syntax highlighting
                if show_file_paths:
                    self.preview_text.insert(tk.END, file_path, "file_path")
                    self.preview_text.insert(tk.END, "\n\n")
                    current_position += len(file_path) + 2  # +2 for newlines
                    all_content += f"{file_path}\n\n"

                self.preview_text.insert(tk.END, f"{prefix_delimiter}\n", "delimiter")
                current_position += len(prefix_delimiter) + 1
                all_content += f"{prefix_delimiter}\n"

                self.preview_text.insert(tk.END, content + "\n")
                current_position += len(content) + 1
                all_content += content + "\n"

                self.preview_text.insert(tk.END, f"{suffix_delimiter}\n\n", "delimiter")
                current_position += len(suffix_delimiter) + 2
                all_content += f"{suffix_delimiter}\n\n"

            pyperclip.copy(all_content)

            # Enhanced status message with file count and total size
            total_size = len(all_content)
            size_str = f"{total_size:,} characters"
            if total_size > 1024:
                size_str = f"{total_size/1024:.1f} KB"
            if total_size > 1024 * 1024:
                size_str = f"{total_size/(1024*1024):.1f} MB"

            self.status_var.set(
                f"✓ Copied {len(actual_files)} files ({size_str}) to clipboard. Uncheck files you don't want and click again to reprocess."
            )

            # Show message box with feedback
            messagebox.showinfo(
                "Success",
                f"Successfully copied {len(actual_files)} files ({size_str}) to clipboard!",
                icon="info",
            )

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}", icon="error")

    def process_selected_files(self):
        """Process only the checked files and copy their content to clipboard."""
        # Get selected files from treeview
        selected_files = []

        def get_checked_files(item):
            values = self.file_tree.item(item, "values")
            if values[0] == "☑":  # Checked
                file_path = values[1]
                if os.path.isfile(file_path):
                    selected_files.append(file_path)
            # Check children recursively
            for child in self.file_tree.get_children(item):
                get_checked_files(child)

        # Start checking from root items
        for item in self.file_tree.get_children():
            get_checked_files(item)

        if not selected_files:
            messagebox.showinfo("Info", "No files selected for copying", icon="info")
            return

        # Filter file data to include only selected files
        selected_data = [
            (path, content)
            for path, content in self.file_data
            if path in selected_files
        ]

        prefix_delimiter = self.prefix_delimiter_var.get()
        suffix_delimiter = self.suffix_delimiter_var.get()
        show_file_paths = self.show_paths_var.get()

        self.preview_text.delete(1.0, tk.END)

        try:
            all_content = ""
            # Store positions for each file in the preview for navigation
            self.file_positions = {}
            current_position = 0

            for file_path, content in selected_data:
                # Store the starting position of this file in the preview
                self.file_positions[file_path] = current_position

                # Insert with syntax highlighting
                if show_file_paths:
                    self.preview_text.insert(tk.END, file_path, "file_path")
                    self.preview_text.insert(tk.END, "\n\n")
                    current_position += len(file_path) + 2  # +2 for newlines
                    all_content += f"{file_path}\n\n"

                self.preview_text.insert(tk.END, f"{prefix_delimiter}\n", "delimiter")
                current_position += len(prefix_delimiter) + 1
                all_content += f"{prefix_delimiter}\n"

                self.preview_text.insert(tk.END, content + "\n")
                current_position += len(content) + 1
                all_content += content + "\n"

                self.preview_text.insert(tk.END, f"{suffix_delimiter}\n\n", "delimiter")
                current_position += len(suffix_delimiter) + 2
                all_content += f"{suffix_delimiter}\n\n"

            pyperclip.copy(all_content)

            # Enhanced status message with file count and total size
            total_size = len(all_content)
            size_str = f"{total_size:,} characters"
            if total_size > 1024:
                size_str = f"{total_size/1024:.1f} KB"
            if total_size > 1024 * 1024:
                size_str = f"{total_size/(1024*1024):.1f} MB"

            self.status_var.set(
                f"✓ Copied {len(selected_data)} files ({size_str}) to clipboard! Click 'Process and Copy' again to update selection."
            )

            # Show message box with feedback
            messagebox.showinfo(
                "Success",
                f"Successfully copied {len(selected_data)} files ({size_str}) to clipboard!",
                icon="info",
            )

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}", icon="error")

    def clear_all(self):
        self.path_var.set("")
        self.file_paths = []
        self.file_data = []
        self.preview_text.delete(1.0, tk.END)
        self.status_var.set("")
        for item in self.file_tree.get_children():
            self.file_tree.delete(item)
        # Reset the button text
        self.process_btn.config(text="Process and Copy")


def main():
    root = tk.Tk()
    # Set initial window size larger
    root.geometry("1000x800")
    # Use system default font
    app = GoogleStyleFileCopyApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
