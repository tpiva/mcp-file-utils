from datetime import datetime
from pydantic import ValidationError
from server import mcp
from pathlib import Path
from constants import errors
from tools.schemas import DirectoryPathParams, FilePathParams

# @mcp.tool()
def list_files(dir_path: str):
    """
    Lists all files in a specified directory.

    This function checks if the provided path is a valid directory and
    returns a list containing the names of all files within it.
    Subdirectories are ignored.

    Args:
        dir_path (str): Path to the directory to be listed.

    Returns:
        Dict[str, Union[bool, str, List[str]]]: Dictionary containing:
            - On success:
                * success (bool): True
                * data (List[str]): List of file names
            - On error:
                * success (bool): False
                * message (str): Error description
                * code (str): Specific error code

    Raises:
        Does not raise exceptions directly, but returns errors in the dictionary.
    """

    try:
        params = DirectoryPathParams(dir_path=dir_path)
    except ValidationError as e:
        return {
            "success": False,
            "message": f"Invalid parameters: {e}",
            "code": errors.VALIDATION_ERROR,
            "errors": e.errors()
        }

    try:
        
        directory_path = Path(params.dir_path)
        file_paths = []
        for entry in directory_path.iterdir():
            if entry.is_file():
                file_paths.append(entry.name)

        return {
                "success": True,
                "message": f"Number of files found: {len(file_paths)}",
                "data": {
                    file_paths
                }
            }
    except (TypeError, ValueError) as e:
        return {
            "success": False,
            "message": f"Invalid path format: {str(e)}",
            "code":  errors.PATH_FORMAT_ERROR,
        }
    
# @mcp.tool()
def read_file_content(file_path: str):
    """
    Read file content based on a path.

    Args:
        file_path (str): Path to the file to be read.

    Returns:
        Dict[str, Union[bool, str, List[str]]]: Dictionary containing:
            - On success:
                * success (bool): True
                * data (List[str]): File Content
            - On error:
                * success (bool): False
                * message (str): Error description
                * code (str): Specific error code

    Raises:
        Does not raise exceptions directly, but returns errors in the dictionary.
    """
    try:
        params = FilePathParams(file_path=file_path)
    except ValidationError as e:
        return {
            "success": False,
            "message": f"Invalid parameters: {e}",
            "code": errors.VALIDATION_ERROR,
            "errors": e.errors()
        }
    
    data = None
    try:
        file_correct_path = Path(params.file_path)
        with open(file_correct_path, 'r', encoding='utf-8', errors='ignore') as file:
            data = file.read()
    except (PermissionError, UnicodeDecodeError, OSError):
        return {
            "success": False,
            "message": f"Invalid parameters: {e}",
            "code": errors.READ_FILE_ERROR,
            "errors": e.errors()
        }

    return {
            "success": True,
            "message": f"Success ready file content and returned in data!",
            "data": {
                "file_content": data
            }
        }

def read_file_attributes(file_path: str):
    """
    Read file statistics by a given path.

    Args:
        file_path (str): Path to the file to be read.

    Returns:
        Dict[str, Union[bool, str, List[str]]]: Dictionary containing:
            - On success:
                * success (bool): True
                * data (Dict): File statistics
            - On error:
                * success (bool): False
                * message (str): Error description
                * code (str): Specific error code

    Raises:
        Does not raise exceptions directly, but returns errors in the dictionary.
    """
    try:
        params = FilePathParams(file_path=file_path)
    except ValidationError as e:
        return {
            "success": False,
            "message": f"Invalid parameters: {e}",
            "code": errors.VALIDATION_ERROR,
            "errors": e.errors()
        }
    
    file = Path(params.file_path)
    statistics = file.stat()

    return {
            "success": True,
            "message": f"Success ready file content and returned in data!",
            "data": {
                "nome": file.name,
                "size_bytes": statistics.st_size,
                "size_mb": round(statistics.st_size / (1024*1024), 2),
                "date_updated": datetime.fromtimestamp(statistics.st_mtime),
                "access": datetime.fromtimestamp(statistics.st_atime),
                "date_created": datetime.fromtimestamp(statistics.st_ctime),
                "is_file": file.is_file(),
                "is_directory": file.is_dir(),
                "permissions": oct(statistics.st_mode)[-3:]
            }
        }