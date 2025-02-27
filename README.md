# File Copier

A desktop utility for efficiently copying and formatting file contents to the clipboard, designed for developers who interact with LLMs and want a faster way to move the content of files to chats.

## Features

- **Efficient File Management**:
  - Process individual files or entire directories
  - Recursive directory processing with a simple checkbox
  - Automatic filtering of system and temporary files
  
- **Customizable Output**:
  - Clear file path presentation
  - Customizable delimiters for content separation
  - Consistent formatting across multiple files
  
- **Intelligent Filtering**:
  - Built-in exclusion of common system files (.DS_Store, __pycache__)
  - User-defined file type exclusions via extension filtering
  - Focus on relevant content files only
  
- **Practical Interface**:
  - Single-screen design for immediate usability
  - Live preview of formatted output
  - Clipboard integration for seamless workflow

## Use Cases

- **Software Development**: Share code snippets or entire modules with structured formatting
- **Documentation**: Format file contents for inclusion in technical documentation
- **Code Analysis**: Prepare code for review or analysis by language models
- **Knowledge Transfer**: Share project structures with clear file delineation
- **Technical Communication**: Facilitate discussion of file-based content with proper context

## Installation

1. Ensure Python 3.6+ is installed
2. Install the required dependency:

```bash
pip install pyperclip
```

## Usage

1. Run the application:

```bash
python3 app.py
```

2. Using the application:
   - Select a file or directory using the browse buttons
   - Configure processing options as needed
   - Click "Process and Copy to Clipboard"
   - Paste formatted content where needed

## Configuration Options

- **Include subdirectories**: Process nested directory structures
- **Show file paths**: Include path information for context
- **Ignore file types**: Specify extensions to exclude (.pyc, .pyo, etc.)
- **Delimiters**: Define start and end markers for each file

## Output Format

The application formats output as follows:

```
/path/to/file.txt

<PREFIX_DELIMITER>
File content appears here...
<SUFFIX_DELIMITER>
```

This structured format maintains clarity when sharing multiple files and integrates well with text analysis systems, including language models.

## Dependencies

- **pyperclip**: Clipboard integration
- **tkinter**: User interface (standard library)
