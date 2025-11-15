import os
from constants import errors
from pydantic import ValidationError
from tools.schemas import CreateNewFolderParams, RenameFileParams
from pathlib import Path

def create_new_folder(dir_path: str, folder_name: str):
    try:
        params = CreateNewFolderParams(dir_path=dir_path, folder_name=folder_name)
    except ValidationError as e:
        return {
            "success": False,
            "message": f"Invalid parameters: {e}",
            "code": errors.VALIDATION_ERROR,
            "errors": e.errors()
        }
    
    try:
        full_folder_path = os.path.join(params.dir_path, params.folder_name)
        Path(full_folder_path).mkdir(exist_ok=True)

        return {
            "success": True,
            "data": {
                "folder_path": full_folder_path
            }
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Error during creating folder {params.folder_name} in path {params.dir_path}",
            "code":  errors.FOLDER_CREATION_ERROR,
        }

def rename_file(file_path: str, new_file_name: str):
    try:
        params = RenameFileParams(file_path=file_path, new_file_name=new_file_name)
    except ValidationError as e:
        return {
            "success": False,
            "message": f"Invalid parameters: {e}",
            "code": errors.VALIDATION_ERROR,
            "errors": e.errors()
        }
    
    try:
        old_file = Path(params.file_path)

        new_file_path = os.path.join(old_file.parent, params.new_file_name)

        old_file.rename(new_file_path)

        return {
            "success": True,
            "data": {
                "old_file": params.file_path,
                "new_file": new_file_path
            }
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"Error during renaming file from {old_file.name} to {params.new_file_name}",
            "code":  errors.RENAME_FILE_ERROR,
        }

    
if __name__ == "__main__":
    data = rename_file(file_path="/Users/thiago.piva/Documents/studies/mcp-file-utils/real_test/first_test.txt", new_file_name="new_first_test.txt")
    print(data)
