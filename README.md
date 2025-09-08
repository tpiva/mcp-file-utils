# MCP File Utils

MCP for interactive with File System.

## Setup

### Prerequisites

- Python 3.11 or higher
- [uv](https://docs.astral.sh/uv/) package manager

### Installation

1. **Navigate to the project directory:**

    ```bash
    cd mcp-file-utils
    ```

2. **Configure Python environment (if using pyenv):**

    ```bash
    # Set the Python version for this project (optional)
    pyenv local 3.11.0  # or your preferred Python 3.11+ version
    
    # Configure uv to use the pyenv Python
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
    ```

## Running the Server

### Standalone Mode (for testing)

To run the server directly for testing:

```bash
uv run mcp-file-utils
```

The server will start and wait for MCP protocol messages via stdin/stdout. Press `Ctrl+C` to stop.

### Develop mode with interactive

To run the server in interactive mode for testing:

```bash
uv run dev mcp src/main.py
```
