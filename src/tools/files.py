import re
import mimetypes
from typing import Dict, List, Union
from pydantic import ValidationError
from server import mcp
from pathlib import Path
from constants import errors
from tools.schemas import ListFileSchema, SearchFileSchema

@mcp.tool()
def search_file(**kwargs) -> Dict[str, Union[bool, str, List[Dict[str, Union[str, int]]]]]:
    """
    Searches for files in a directory by filename or content.

    This function searches through files in the specified directory and can
    match files by filename, file content, or both. It supports recursive
    search and filtering by file extensions.

    Args:
        dir_path (str): Path to the directory to search in.
        search_term (str): Term to search for in filenames or content.
        search_by (str, optional): Search mode. Options are:
            - "name": Search only in filenames (default)
            - "content": Search only in file contents
        case_sensitive (bool, optional): Whether to perform case-sensitive search. 
            Defaults to False.
        recursive (bool, optional): Whether to search subdirectories recursively. 
            Defaults to True.
        file_extension (str, optional): Search only by txt file extension

    Returns:
        Dict[str, Union[bool, str, List[Dict[str, Union[str, int]]]]]: Dictionary containing:
            - On success:
                * success (bool): True
                * data (List[Dict]): List of matching files with details:
                    - file_path (str): Full path to the file
                    - match_type (str): "name", "content", or "both"
                    - line_number (int): Line where content was found (if applicable)
                    - matched_line (str): The actual line content (if applicable)
            - On error:
                * success (bool): False
                * message (str): Error description
                * code (str): Specific error code

    Raises:
        TypeError: If dir_path is not a string or path-like object.
        ValueError: If search_by parameter has invalid value.

    """
    try:
        params = SearchFileSchema(**kwargs)
    except ValidationError as e:
        return {
            "success": False,
            "message": f"Invalid parameters: {e}",
            "code": errors.VALIDATION_ERROR,
            "errors": e.errors()
        }
    
    matches = []
    search_pattern = re.compile(
        re.escape(params.search_term), 
        0 if params.case_sensitive else re.IGNORECASE
    )

    directory_path = Path(params.dir_path)
    search_method = directory_path.rglob("*") if params.recursive else directory_path.iterdir()

    for file_path in search_method:
        if not file_path.is_file():
            continue
        
        file_match = {
                "file_path": str(file_path),
                "match_type": None,
                "line_number": None,
                "matched_line": None
            }
    
        if params.search_by == "name":
            if search_pattern.search(file_path.name):
                matches.append({
                    **file_match,
                    "match_type": "name"
                })
            
        if params.search_by == "content":
            try:
                mime_type, _ = mimetypes.guess_type(str(file_path))
                if mime_type and not mime_type.startswith('text'):
                    continue
                
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                    for line_num, line in enumerate(file, 1):
                        if search_pattern.search(line):
                            matches.append({
                                **file_match,
                                "match_type": "content",
                                "line_number": line_num,
                                "matched_line": line.strip()
                            })
                            content_match = file_match.copy()
                            content_match["match_type"] = "content" if file_match["match_type"] != "name" else "both"
                            content_match["line_number"] = line_num
                            content_match["matched_line"] = line.strip()
                            break
                            
            except (PermissionError, UnicodeDecodeError, OSError):
                continue

        return {
                "success": True,
                "message": f"Search by {params.search_by} found total #{len(matches)} results",
                "data": matches
            }

@mcp.tool()
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
        params = ListFileSchema(dir_path=dir_path)
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
                "data": file_paths
            }
    except (TypeError, ValueError) as e:
        return {
            "success": False,
            "message": f"Invalid path format: {str(e)}",
            "code":  errors.PATH_FORMAT_ERROR,
        }
    

