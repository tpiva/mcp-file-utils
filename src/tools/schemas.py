from typing import Any, Union
from pydantic import BaseModel, field_validator
from pathlib import Path

class SearchFileSchema(BaseModel):
    dir_path: str
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
    
    @field_validator('dir_path')
    @classmethod
    def validate_dir_path(cls, v: str) -> str:
        directory_path = Path(v)
        if not directory_path.exists():
            raise ValueError(f'Directory does not exist: {v}')
        if not directory_path.is_dir():
            raise ValueError(f'Path is not a directory: {v}')
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
    
class ListFileSchema(BaseModel):
    dir_path: str

    @field_validator('dir_path')
    @classmethod
    def validate_dir_path(cls, v: str) -> str:
        directory_path = Path(v)
        if not directory_path.exists():
            raise ValueError(f'Directory does not exist: {v}')
        if not directory_path.is_dir():
            raise ValueError(f'Path is not a directory: {v}')
        return v