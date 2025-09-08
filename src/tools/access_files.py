from server import mcp

@mcp.tool()
def testing() -> str:
    """
    A simple testing tool to verify MCP server functionality.
    
    Returns:
        str: A success message indicating the tool is working
    """
    return "Testing tool is working correctly! MCP server is functional."