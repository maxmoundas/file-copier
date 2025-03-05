import tkinter as tk
from tkinter import filedialog, scrolledtext, ttk, messagebox
import os
import pyperclip
from pathlib import Path


class FileCopyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Content Copier")
        self.root.geometry("800x700")
        self.root.minsize(600, 500)

        self.setup_ui()

    def setup_ui(self):
        # Create main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Path selection section
        path_frame = ttk.LabelFrame(
            main_frame, text="Select File or Directory", padding="10"
        )
        path_frame.pack(fill=tk.X, padx=5, pady=5)

        self.path_var = tk.StringVar()
        path_entry = ttk.Entry(path_frame, textvariable=self.path_var, width=50)
        path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

        browse_file_btn = ttk.Button(
            path_frame, text="Browse File(s)", command=self.browse_file
        )
        browse_file_btn.pack(side=tk.LEFT, padx=2)

        browse_dir_btn = ttk.Button(
            path_frame, text="Browse Directory", command=self.browse_directory
        )
        browse_dir_btn.pack(side=tk.LEFT, padx=2)

        # Options section
        options_frame = ttk.LabelFrame(main_frame, text="Options", padding="10")
        options_frame.pack(fill=tk.X, padx=5, pady=5)

        # Directory options
        self.recursive_var = tk.BooleanVar(value=False)
        recursive_check = ttk.Checkbutton(
            options_frame, text="Include subdirectories", variable=self.recursive_var
        )
        recursive_check.grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)

        self.show_paths_var = tk.BooleanVar(value=True)
        show_paths_check = ttk.Checkbutton(
            options_frame, text="Show file paths", variable=self.show_paths_var
        )
        show_paths_check.grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)

        # File type ignore option
        ttk.Label(options_frame, text="Ignore file types:").grid(
            row=2, column=0, sticky=tk.W, padx=5, pady=2
        )
        self.ignore_types_var = tk.StringVar(value="")
        ignore_types_entry = ttk.Entry(
            options_frame, textvariable=self.ignore_types_var, width=30
        )
        ignore_types_entry.grid(
            row=2, column=1, columnspan=2, sticky=tk.W, padx=5, pady=2
        )
        ttk.Label(options_frame, text="(comma-separated extensions)").grid(
            row=3, column=1, columnspan=2, sticky=tk.W, padx=5, pady=0
        )

        # Delimiter options
        ttk.Label(options_frame, text="Prefix delimiter:").grid(
            row=0, column=1, sticky=tk.E, padx=5, pady=2
        )
        self.prefix_delimiter_var = tk.StringVar(value="```")
        prefix_entry = ttk.Entry(
            options_frame, textvariable=self.prefix_delimiter_var, width=15
        )
        prefix_entry.grid(row=0, column=2, padx=5, pady=2)

        ttk.Label(options_frame, text="Suffix delimiter:").grid(
            row=1, column=1, sticky=tk.E, padx=5, pady=2
        )
        self.suffix_delimiter_var = tk.StringVar(value="```")
        suffix_entry = ttk.Entry(
            options_frame, textvariable=self.suffix_delimiter_var, width=15
        )
        suffix_entry.grid(row=1, column=2, padx=5, pady=2)

        # Action buttons
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(fill=tk.X, padx=5, pady=5)

        process_btn = ttk.Button(
            action_frame,
            text="Process and Copy to Clipboard",
            command=self.process_path,
        )
        process_btn.pack(side=tk.LEFT, padx=5)

        clear_btn = ttk.Button(action_frame, text="Clear", command=self.clear_all)
        clear_btn.pack(side=tk.LEFT, padx=5)

        # Preview section
        preview_frame = ttk.LabelFrame(main_frame, text="Preview", padding="10")
        preview_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.preview_text = scrolledtext.ScrolledText(
            preview_frame, wrap=tk.WORD, height=20
        )
        self.preview_text.pack(fill=tk.BOTH, expand=True)

        # Status bar
        self.status_var = tk.StringVar()
        status_bar = ttk.Label(
            main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W
        )
        status_bar.pack(fill=tk.X, side=tk.BOTTOM, padx=5, pady=2)

        # Store multiple file paths
        self.file_paths = []

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
        results = []
        errors = []

        files_to_process = []

        if self.recursive_var.get():
            for root, dirs, files in os.walk(directory_path):
                # Skip __pycache__ directories
                if "__pycache__" in dirs:
                    dirs.remove("__pycache__")

                # Skip other common directories to ignore
                for ignore_dir in [
                    ".git",
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

        for file_path in files_to_process:
            try:
                content = self.read_file(file_path)
                results.append((file_path, content))
            except Exception as e:
                errors.append((file_path, str(e)))

        return results, errors

    def process_files(self, file_paths):
        """Process multiple files and return their contents."""
        results = []
        errors = []

        for file_path in file_paths:
            if not self.should_ignore_file(file_path):
                try:
                    content = self.read_file(file_path)
                    results.append((file_path, content))
                except Exception as e:
                    errors.append((file_path, str(e)))

        return results, errors

    def process_path(self):
        path = self.path_var.get().strip()

        if not path and not self.file_paths:
            messagebox.showerror(
                "Error", "Please enter or select a file/directory path"
            )
            return

        # Check if we have multiple files selected
        if self.file_paths and len(self.file_paths) > 1:
            # Process multiple files
            file_paths = self.file_paths
        else:
            # Single file or directory path
            if path.startswith("Selected ") and " files" in path:
                # We have multiple files but need to use the stored paths
                file_paths = self.file_paths
            else:
                # Regular single path processing
                if not os.path.exists(path):
                    messagebox.showerror("Error", "Path does not exist")
                    return
                if os.path.isdir(path):
                    file_paths = []  # Will be handled by process_directory
                else:
                    file_paths = [path]

        prefix_delimiter = self.prefix_delimiter_var.get()
        suffix_delimiter = self.suffix_delimiter_var.get()
        show_file_paths = self.show_paths_var.get()

        self.preview_text.delete(1.0, tk.END)

        try:
            if file_paths and not os.path.isdir(path):
                # Process multiple files
                results, errors = self.process_files(file_paths)
            elif os.path.isdir(path):
                # Process directory
                results, errors = self.process_directory(path)
            else:
                # Should never reach here
                messagebox.showerror("Error", "Invalid path configuration")
                return

            if results:
                all_content = ""
                for file_path, content in results:
                    if show_file_paths:
                        all_content += f"{file_path}\n\n"
                    all_content += f"{prefix_delimiter}\n"
                    all_content += content + "\n"
                    all_content += f"{suffix_delimiter}\n\n"

                pyperclip.copy(all_content)
                self.preview_text.insert(tk.END, all_content)
                self.status_var.set(f"Copied {len(results)} files to clipboard!")

                if errors:
                    error_msg = "Some files could not be processed:\n"
                    for file_path, error in errors:
                        error_msg += f"\n{file_path}: {error}"
                    messagebox.showwarning("Warnings", error_msg)
            else:
                if errors:
                    error_msg = "No files were processed. Errors:\n"
                    for file_path, error in errors:
                        error_msg += f"\n{file_path}: {error}"
                    messagebox.showerror("Error", error_msg)
                else:
                    messagebox.showinfo("Info", "No files found to process")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def clear_all(self):
        self.path_var.set("")
        self.file_paths = []
        self.preview_text.delete(1.0, tk.END)
        self.status_var.set("")


def main():
    root = tk.Tk()
    app = FileCopyApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
