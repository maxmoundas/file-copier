import tkinter as tk
from tkinter import filedialog, scrolledtext, ttk, messagebox
import os
import pyperclip
from pathlib import Path


class ModernFileCopyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Content Copier")
        self.root.geometry("900x750")
        self.root.minsize(700, 600)

        # Set theme colors
        self.colors = {
            "bg_dark": "#2E3440",
            "bg_medium": "#3B4252",
            "bg_light": "#434C5E",
            "accent": "#5E81AC",
            "accent_hover": "#81A1C1",
            "text_light": "#ECEFF4",
            "text_dark": "#D8DEE9",
            "success": "#A3BE8C",
            "warning": "#EBCB8B",
            "error": "#BF616A",
        }

        # Configure style
        self.style = ttk.Style()
        self.style.theme_use("default")

        # Configure colors
        self.root.configure(bg=self.colors["bg_dark"])

        # Configure styles for widgets
        self.configure_styles()

        self.setup_ui()

    def configure_styles(self):
        # Configure frame styles
        self.style.configure("TFrame", background=self.colors["bg_dark"])
        self.style.configure(
            "Card.TFrame",
            background=self.colors["bg_medium"],
            relief="flat",
            borderwidth=0,
        )

        # Configure label styles
        self.style.configure(
            "TLabel",
            background=self.colors["bg_dark"],
            foreground=self.colors["text_light"],
            font=("Segoe UI", 10),
        )
        self.style.configure("Header.TLabel", font=("Segoe UI", 12, "bold"))
        self.style.configure("Subheader.TLabel", font=("Segoe UI", 11))

        # Configure button styles
        self.style.configure(
            "TButton",
            background=self.colors["accent"],
            foreground=self.colors["text_light"],
            font=("Segoe UI", 10),
            relief="flat",
            borderwidth=0,
        )
        self.style.map(
            "TButton",
            background=[("active", self.colors["accent_hover"])],
            relief=[("pressed", "sunken")],
        )

        # Primary button style
        self.style.configure("Primary.TButton", font=("Segoe UI", 10, "bold"))

        # Configure entry styles
        self.style.configure(
            "TEntry",
            fieldbackground=self.colors["bg_light"],
            foreground=self.colors["text_light"],
            insertcolor=self.colors["text_light"],
            borderwidth=0,
            relief="flat",
        )

        # Configure checkbox styles
        self.style.configure(
            "TCheckbutton",
            background=self.colors["bg_dark"],
            foreground=self.colors["text_light"],
            font=("Segoe UI", 10),
        )

        self.style.map(
            "TCheckbutton",
            background=[("active", self.colors["bg_dark"])],
            indicatorcolor=[
                ("selected", self.colors["accent"]), 
                ("!selected", self.colors["bg_light"])
            ],
            indicatorrelief=[("pressed", "sunken"), ("!pressed", "raised")],
        )

        # Configure treeview styles
        self.style.configure(
            "Treeview",
            background=self.colors["bg_medium"],
            foreground=self.colors["text_light"],
            fieldbackground=self.colors["bg_medium"],
            font=("Segoe UI", 10),
        )
        self.style.configure(
            "Treeview.Heading",
            background=self.colors["bg_light"],
            foreground=self.colors["text_light"],
            font=("Segoe UI", 10, "bold"),
            relief="flat",
        )
        self.style.map(
            "Treeview.Heading", background=[("active", self.colors["accent"])]
        )
        self.style.map("Treeview", background=[("selected", self.colors["accent"])])

        # Configure scrollbar styles
        self.style.configure(
            "Vertical.TScrollbar",
            background=self.colors["bg_light"],
            troughcolor=self.colors["bg_medium"],
            arrowcolor=self.colors["text_light"],
        )

        # Configure labelframe styles
        self.style.configure("TLabelframe", background=self.colors["bg_dark"])
        self.style.configure(
            "TLabelframe.Label",
            background=self.colors["bg_dark"],
            foreground=self.colors["text_light"],
            font=("Segoe UI", 11, "bold"),
        )

    def setup_ui(self):
        # Add padding around the main window
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Create rounded card containers with padding
        self.create_path_section(main_frame)
        self.create_options_section(main_frame)
        self.create_action_section(main_frame)

        # Create a paned window with better proportions
        paned_window = ttk.PanedWindow(main_frame, orient=tk.VERTICAL)
        paned_window.pack(fill=tk.BOTH, expand=True, pady=(10, 5))

        self.create_file_selection_section(paned_window)
        self.create_preview_section(paned_window)

        # Status bar
        status_frame = ttk.Frame(main_frame)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=(5, 0))

        self.status_var = tk.StringVar()
        status_bar = ttk.Label(
            status_frame,
            textvariable=self.status_var,
            background=self.colors["bg_medium"],
            foreground=self.colors["text_light"],
            padding=(10, 5),
        )
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)

        # Store multiple file paths and data
        self.file_paths = []
        self.file_data = []
        self.file_positions = {}

    def create_rounded_frame(self, parent, title=None):
        """Create a rounded frame with custom styling"""
        if title:
            frame = ttk.LabelFrame(parent, text=title, padding="15")
        else:
            frame = ttk.Frame(parent, padding="15", style="Card.TFrame")

        return frame

    def create_path_section(self, parent):
        path_frame = self.create_rounded_frame(parent, "Select File or Directory")
        path_frame.pack(fill=tk.X, pady=(0, 10))

        self.path_var = tk.StringVar()
        path_entry = ttk.Entry(
            path_frame, textvariable=self.path_var, width=50, font=("Segoe UI", 10)
        )
        path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

        # Add some spacing between buttons
        button_frame = ttk.Frame(path_frame)
        button_frame.pack(side=tk.RIGHT)

        browse_file_btn = ttk.Button(
            button_frame, text=" Browse File(s) ", command=self.browse_file
        )
        browse_file_btn.pack(side=tk.LEFT, padx=(0, 5))

        browse_dir_btn = ttk.Button(
            button_frame, text=" Browse Directory ", command=self.browse_directory
        )
        browse_dir_btn.pack(side=tk.LEFT)

    def create_options_section(self, parent):
        options_frame = self.create_rounded_frame(parent, "Options")
        options_frame.pack(fill=tk.X, pady=(0, 10))

        # Create a grid with better spacing
        options_frame.columnconfigure(0, weight=1)
        options_frame.columnconfigure(1, weight=1)
        options_frame.columnconfigure(2, weight=1)

        # Directory options
        self.recursive_var = tk.BooleanVar(value=False)
        recursive_check = ttk.Checkbutton(
            options_frame, text="Include subdirectories", variable=self.recursive_var
        )
        recursive_check.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)

        self.show_paths_var = tk.BooleanVar(value=True)
        show_paths_check = ttk.Checkbutton(
            options_frame, text="Show file paths", variable=self.show_paths_var
        )
        show_paths_check.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)

        # File type ignore option with better alignment
        ignore_label = ttk.Label(options_frame, text="Ignore file types:")
        ignore_label.grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)

        self.ignore_types_var = tk.StringVar(value="")
        ignore_types_entry = ttk.Entry(
            options_frame,
            textvariable=self.ignore_types_var,
            width=30,
            font=("Segoe UI", 10),
        )
        ignore_types_entry.grid(
            row=2, column=1, columnspan=2, sticky=tk.W, padx=5, pady=5
        )

        info_label = ttk.Label(
            options_frame, text="(comma-separated extensions)", font=("Segoe UI", 9)
        )
        info_label.grid(row=3, column=1, columnspan=2, sticky=tk.W, padx=5, pady=(0, 5))

        # Delimiter options with better alignment
        prefix_label = ttk.Label(options_frame, text="Prefix delimiter:")
        prefix_label.grid(row=0, column=1, sticky=tk.E, padx=5, pady=5)

        self.prefix_delimiter_var = tk.StringVar(value="```")
        prefix_entry = ttk.Entry(
            options_frame,
            textvariable=self.prefix_delimiter_var,
            width=15,
            font=("Segoe UI", 10),
        )
        prefix_entry.grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)

        suffix_label = ttk.Label(options_frame, text="Suffix delimiter:")
        suffix_label.grid(row=1, column=1, sticky=tk.E, padx=5, pady=5)

        self.suffix_delimiter_var = tk.StringVar(value="```")
        suffix_entry = ttk.Entry(
            options_frame,
            textvariable=self.suffix_delimiter_var,
            width=15,
            font=("Segoe UI", 10),
        )
        suffix_entry.grid(row=1, column=2, padx=5, pady=5, sticky=tk.W)

    def create_action_section(self, parent):
        action_frame = ttk.Frame(parent)
        action_frame.pack(fill=tk.X, pady=(0, 10))

        self.process_btn = ttk.Button(
            action_frame,
            text="Process and Copy to Clipboard",
            command=self.process_path,
            style="Primary.TButton",
        )
        self.process_btn.pack(side=tk.LEFT, padx=(0, 10))

        clear_btn = ttk.Button(action_frame, text="Clear", command=self.clear_all)
        clear_btn.pack(side=tk.LEFT)

    def create_file_selection_section(self, parent):
        file_list_frame = self.create_rounded_frame(parent, "File Selection")
        parent.add(file_list_frame, weight=1)

        # Controls for file selection
        controls_frame = ttk.Frame(file_list_frame)
        controls_frame.pack(fill=tk.X, pady=(0, 10))

        select_all_btn = ttk.Button(
            controls_frame, text="Select All", command=self.select_all_files
        )
        select_all_btn.pack(side=tk.LEFT, padx=(0, 5))

        deselect_all_btn = ttk.Button(
            controls_frame, text="Deselect All", command=self.deselect_all_files
        )
        deselect_all_btn.pack(side=tk.LEFT)

        # File list with better styling
        tree_frame = ttk.Frame(file_list_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        # Add scrollbar for file list
        file_list_scrollbar = ttk.Scrollbar(tree_frame, style="Vertical.TScrollbar")
        file_list_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Create treeview for file list with checkboxes
        self.file_tree = ttk.Treeview(
            tree_frame,
            columns=("checked", "path"),
            show="headings",
            selectmode="browse",
            yscrollcommand=file_list_scrollbar.set,
        )
        self.file_tree.heading("checked", text="Include")
        self.file_tree.heading("path", text="File Path")
        self.file_tree.column("checked", width=80, anchor=tk.CENTER)
        self.file_tree.column("path", width=500)
        self.file_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        file_list_scrollbar.config(command=self.file_tree.yview)

        # Bind click event to toggle checkbox
        self.file_tree.bind("<ButtonRelease-1>", self.toggle_checkbox)

        # Bind click event for selection to scroll preview
        self.file_tree.bind("<<TreeviewSelect>>", self.scroll_to_file_in_preview)

    def create_preview_section(self, parent):
        preview_frame = self.create_rounded_frame(parent, "Preview")
        parent.add(preview_frame, weight=1)

        # Custom styled preview text
        self.preview_text = scrolledtext.ScrolledText(
            preview_frame,
            wrap=tk.WORD,
            height=10,
            bg=self.colors["bg_medium"],
            fg=self.colors["text_light"],
            insertbackground=self.colors["text_light"],
            selectbackground=self.colors["accent"],
            font=("Consolas", 10),
        )
        self.preview_text.pack(fill=tk.BOTH, expand=True)

        # Configure tags for syntax highlighting
        self.preview_text.tag_configure("highlight", background="#3a4466")
        self.preview_text.tag_configure(
            "file_path", foreground="#A3BE8C", font=("Consolas", 10, "bold")
        )
        self.preview_text.tag_configure(
            "delimiter", foreground="#81A1C1", font=("Consolas", 10)
        )
        self.highlight_tag_configured = True

    def toggle_checkbox(self, event):
        item = self.file_tree.identify_row(event.y)
        column = self.file_tree.identify_column(event.x)

        if not item or column != "#1":  # First column is checkbox
            return

        current_value = self.file_tree.item(item, "values")[0]
        new_value = "☐" if current_value == "☑" else "☑"
        values = list(self.file_tree.item(item, "values"))
        values[0] = new_value
        self.file_tree.item(item, values=values)

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
                "Info", "Enable 'Show file paths' option to use this feature"
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

        # Always ignore .DS_Store
        if file_name == ".DS_Store":
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

    def process_directory(self, directory_path):
        """Process all files in a directory and return their contents."""
        files_to_process = []

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

                for file in files:
                    file_path = os.path.join(root, file)
                    if not self.should_ignore_file(file_path):
                        files_to_process.append(file_path)
        else:
            for item in os.listdir(directory_path):
                # Skip __pycache__ directories
                if item == "__pycache__":
                    continue

                file_path = os.path.join(directory_path, item)
                if os.path.isfile(file_path) and not self.should_ignore_file(file_path):
                    files_to_process.append(file_path)

        return files_to_process

    def get_files_to_scan(self):
        """Get the list of files to scan based on user selection."""
        path = self.path_var.get().strip()

        if not path and not self.file_paths:
            messagebox.showerror(
                "Error", "Please enter or select a file/directory path"
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
                    messagebox.showerror("Error", "Path does not exist")
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
                "Error", "Please enter or select a file/directory path"
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

        # Process all files first
        for file_path in files_to_scan:
            if not self.should_ignore_file(file_path):
                try:
                    # Read file content
                    content = self.read_file(file_path)
                    # Add to file data
                    self.file_data.append((file_path, content))
                    # Add to treeview with checkbox
                    self.file_tree.insert("", "end", values=["☑", file_path])
                except Exception as e:
                    errors.append((file_path, str(e)))

        if not self.file_data:
            if errors:
                error_msg = "No files were processed. Errors:\n"
                for file_path, error in errors:
                    error_msg += f"\n{file_path}: {error}"
                messagebox.showerror("Error", error_msg)
            else:
                messagebox.showinfo("Info", "No files found to process")
            return

        # Copy all files to clipboard on first run
        self.process_all_files()

        # Update status and button text to reflect that files can now be selectively processed
        self.status_var.set(
            f"Copied {len(self.file_data)} files to clipboard. Uncheck files you don't want and click again to reprocess."
        )
        self.process_btn.config(text="Reprocess Selected Files")

        if errors:
            error_msg = "Some files could not be processed:\n"
            for file_path, error in errors:
                error_msg += f"\n{file_path}: {error}"
            messagebox.showwarning("Warnings", error_msg)

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

            for file_path, content in self.file_data:
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
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def process_selected_files(self):
        """Process only the checked files and copy their content to clipboard."""
        # Get selected files from treeview
        selected_files = []
        for item in self.file_tree.get_children():
            values = self.file_tree.item(item, "values")
            if values[0] == "☑":  # Checked
                selected_files.append(values[1])  # File path

        if not selected_files:
            messagebox.showinfo("Info", "No files selected for copying")
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
            self.status_var.set(f"Copied {len(selected_data)} files to clipboard!")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def clear_all(self):
        self.path_var.set("")
        self.file_paths = []
        self.file_data = []
        self.preview_text.delete(1.0, tk.END)
        self.status_var.set("")
        for item in self.file_tree.get_children():
            self.file_tree.delete(item)
        # Reset the button text
        self.process_btn.config(text="Process and Copy to Clipboard")


def main():
    root = tk.Tk()
    app = ModernFileCopyApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
