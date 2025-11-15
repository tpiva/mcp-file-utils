import os
from typing import Any, Union
from pydantic import BaseModel, Field, field_validator
from pathlib import Path


def validate_directory_path(cls, v: str) -> str:
    """Validate robust for directory path"""
    if not v or not v.strip():
        raise ValueError('Directory path cannot be empty')
    
    directory_path = Path(v).resolve()
    
    if not directory_path.exists():
        raise ValueError(f'Directory does not exist: {directory_path}')
    
    if not directory_path.is_dir():
        raise ValueError(f'Path is not a directory: {directory_path}')
    
    if not os.access(directory_path, os.R_OK):
        raise ValueError(f'No read permission for directory: {directory_path}')
    
    return str(directory_path)

def validate_file_path(cls, v: str) -> str:
        file = Path(v)
        if not file.exists():
            raise ValueError(f'File does not exist: {v}')
        if not file.is_file():
            raise ValueError(f'Path is not a file: {v}')
        return v

def validate_txt_file(v: str) -> str:
    if ".txt" not in v:
        raise ValueError('file_name MUST be a txt file')
    return v

class DirectoryPathParams(BaseModel):
    dir_path: str
    
    _validate_dir_path = field_validator('dir_path')(validate_directory_path)

class FilePathParams(BaseModel):
    file_path: str

    _validate_file_path = field_validator('file_path')(validate_file_path)

class SearchFileParams(DirectoryPathParams):
    search_term: str
    search_by: str
    case_sensitive: bool = False
    recursive: bool = True
    file_extension: Union [ str , None ]

    @field_validator('search_by')
    @classmethod
    def validate_search_by(cls, v: str) -> str:
        allowed = ['name', 'content']
        if v not in allowed:
            raise ValueError(f'search_by must be one of: {", ".join(allowed)}')
        return v
    
    @field_validator('file_extension')
    @classmethod
    def validate_file_extension(cls, v: str) -> str:
        allowed_extensions = ['txt']
        if v not in allowed_extensions:
            raise ValueError(f'Extension not allow: {v}')
        return v
    
    @field_validator('search_term')
    @classmethod
    def validate_search_term(cls, v):
        if not v.strip():
            raise ValueError('search_term cannot be empty')
        return v.strip()

class WriteFileParams(DirectoryPathParams):
    file_name: str
    file_content: str = Field(min_length=10, max_length=200)
    append_content: bool

    _validate_file_name = field_validator('file_name')(validate_txt_file)
    
class CreateNewFolderParams(DirectoryPathParams):
    folder_name: str = Field(min_length=3)

class RenameFileParams(FilePathParams):
    new_file_name: str

    _validate_new_file_name = field_validator('new_file_name')(validate_txt_file)