import os
from constants.errors import FILE_CREATION_ERROR, VALIDATION_ERROR
from pydantic import ValidationError
from server import mcp

from tools.schemas import WriteFileParams

# @mcp.tool()
def create_file(dir_path: str, file_name: str, file_content: str, append_content: bool) -> str:
    try:
        params = WriteFileParams(dir_path=dir_path, file_name=file_name, file_content=file_content, append_content=append_content)
    except ValidationError as e:
        return {
            "success": False,
            "message": f"Invalid parameters: {e}",
            "code": VALIDATION_ERROR,
            "errors": e.errors()
        }
    
    full_file_path = os.path.join(params.dir_path, params.file_name)

    try:
        type_file_op = "a" if params.append_content else "w"
        with open(full_file_path, type_file_op) as file:
            file.write(params.file_content)
    except Exception as e:
        return {
            "success": False,
            "message": f"Error during creating a file: {e}",
            "code": FILE_CREATION_ERROR,
            "errors": e
        }
    
    return {
            "success": True,
            "message": f"Success create file with initial content!",
            "data": {
                "name": file.name,
                "initial_content": params.file_content
            }
        }