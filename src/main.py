import logging
from server import mcp

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    return logging.getLogger(__name__)

def main():
    logger = setup_logging()
    logger.info("Initializing MCP server")

    logger.info("Tools imported successfully")
    
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
