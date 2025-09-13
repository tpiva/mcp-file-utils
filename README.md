# MCP File Utils 📁

A powerful Model Context Protocol (MCP) server for advanced file system operations. This tool provides intelligent file search and directory listing capabilities with support for content-based searches, pattern matching, and flexible filtering options.

## 🚀 Features

### 🔍 **Smart File Search** (`search_file`)

- **Multi-mode search**: Search by filename, file content, or both
- **Flexible filtering**: Filter by file extensions (e.g., `.py`, `.txt`, `.json`)
- **Recursive search**: Optionally search through subdirectories
- **Case sensitivity control**: Toggle between case-sensitive and case-insensitive searches
- **Content matching**: Find files containing specific text or patterns
- **Safe regex handling**: Automatic escaping of special characters for literal searches
- **Detailed results**: Returns file paths, match types, line numbers, and matched content

### 📂 **Directory Listing** (`list_files`)

- **Simple directory listing**: Get all files in a specified directory
- **Clean output**: Returns only file names (excludes subdirectories)
- **Error handling**: Validates directory paths and provides clear error messages
- **Fast operation**: Optimized for quick directory scanning

## 🛠️ Setup

### Prerequisites

- **Python 3.11+** - Required for modern type hints and performance improvements
- **[uv](https://docs.astral.sh/uv/)** - Fast Python package manager for dependency management

### Installation

1. **Clone and navigate to the project:**

   ```bash
   git clone <repository-url>
   cd mcp-file-utils
   ```

2. **Configure Python environment (optional with pyenv):**

   ```bash
   # Set Python version for this project
   pyenv local 3.11.0  # or your preferred Python 3.11+ version
   
   # Configure uv to use the correct Python version
   uv python install 3.11
   uv venv --python 3.11
   ```

3. **Install dependencies:**

   ```bash
   uv sync
   ```

4. **Verify installation:**

   ```bash
   uv run python --version
   # Should output: Python 3.11.x or higher
   ```

## 🏃‍♂️ Running the Server

### Production Mode

For production use with MCP clients:

```bash
uv run mcp-file-utils
```

The server starts in MCP protocol mode, communicating via stdin/stdout. Use `Ctrl+C` to stop.

### Development Mode

For testing and development with interactive debugging:

```bash
uv run dev mcp src/main.py
```

This mode provides enhanced logging and debugging capabilities.

## 📖 Available Tools

### 🔍 `search_file`

**Advanced file search with multiple criteria and filtering options.**

#### Parameters

- `dir_path` (str): Directory path to search in
- `search_term` (str): Text to search for
- `search_by` (str, optional): Search mode - `"name"`, `"content"`, or `"both"` (default: `"both"`)
- `case_sensitive` (bool, optional): Enable case-sensitive search (default: `False`)
- `recursive` (bool, optional): Search subdirectories recursively (default: `True`)
- `file_extensions` (List[str], optional): Filter by file extensions (e.g., `[".py", ".txt"]`)

#### Example Usage

```python
# Search for Python files containing "import"
search_file(
    dir_path="/project",
    search_term="import",
    search_by="content",
    file_extensions=[".py"]
)

# Case-sensitive search for files with "Config" in name
search_file(
    dir_path="/app",
    search_term="Config",
    search_by="name",
    case_sensitive=True,
    recursive=False
)

# Find TODO comments in any text file
search_file(
    dir_path="/src",
    search_term="TODO",
    search_by="content",
    file_extensions=[".py", ".js", ".txt"]
)
```

#### Response Format

```json
{
  "success": true,
  "data": [
    {
      "file_path": "/project/main.py",
      "match_type": "content",
      "line_number": 15,
      "matched_line": "import os  # TODO: optimize this"
    }
  ]
}
```

### 📂 `list_files`

**Simple and fast directory listing for file discovery.**

#### Parameters

- `dir_path` (str): Path to the directory to list

#### Example Usage

```python
# List all files in current directory
list_files(dir_path="./")

# List files in specific directory
list_files(dir_path="/home/user/documents")
```

#### Response Format

```json
{
  "success": true,
  "data": ["file1.txt", "script.py", "config.json"]
}
```

## 🔧 Error Handling

Both tools provide comprehensive error handling:

- **Invalid directory paths**: Clear error messages for non-existent directories
- **Permission errors**: Graceful handling of restricted files/directories
- **Invalid parameters**: Validation with specific error codes
- **File encoding issues**: Automatic fallback for unreadable files

### Example Error Response

```json
{
  "success": false,
  "message": "Directory does not exist: /invalid/path",
  "code": "DIR_NOT_EXISTS"
}
```

## 🚀 Use Cases

- **Code Analysis**: Find specific patterns or imports in source code
- **Documentation Search**: Locate files containing specific terms or topics
- **Configuration Management**: Search for configuration files and settings
- **Log Analysis**: Find log files with specific error messages or patterns
- **Project Exploration**: Quick directory listing and file discovery
- **Refactoring**: Find all files that need updates when changing APIs
- **Security Audits**: Search for sensitive information or patterns in codebases

## 📋 Requirements

- Python 3.11+
- `pathlib` (built-in)
- `re` (built-in)  
- `mimetypes` (built-in)
- `pydantic` (for parameter validation)

