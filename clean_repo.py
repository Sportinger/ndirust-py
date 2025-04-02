#!/usr/bin/env python
"""
Repository cleaning script.

This script removes build artifacts, temporary files, and other items that should
not be committed to the GitHub repository.
"""

import os
import shutil
import glob
from pathlib import Path

# Directories to remove completely
DIRS_TO_REMOVE = [
    "target",
    "dist",
    "build",
    "__pycache__",
    ".pytest_cache",
    ".venv",
    "venv",
    "env",
    "ndi",
    "temp_extract",
    "test_extract",
]

# File patterns to remove
FILE_PATTERNS = [
    "**/*.pyc",
    "**/*.pyo",
    "**/*.pyd",
    "**/*.so",
    "**/*.egg-info",
    "**/*.egg",
    "**/*.whl",
    "**/*.bak",
    "**/*.tmp",
]

def clean_directory(base_path):
    """Clean up a directory by removing specified files and directories."""
    base_path = Path(base_path)
    
    # Process directories to remove
    for dir_name in DIRS_TO_REMOVE:
        dir_path = base_path / dir_name
        if dir_path.exists() and dir_path.is_dir():
            print(f"Removing directory: {dir_path}")
            shutil.rmtree(dir_path, ignore_errors=True)
    
    # Process file patterns to remove
    for pattern in FILE_PATTERNS:
        for file_path in base_path.glob(pattern):
            if file_path.is_file():
                print(f"Removing file: {file_path}")
                file_path.unlink()

if __name__ == "__main__":
    # Clean from the repository root directory
    repo_root = Path(__file__).parent.absolute()
    
    print(f"Cleaning repository: {repo_root}")
    clean_directory(repo_root)
    
    print("Repository cleaned successfully!")
    print("Now you can commit your changes to GitHub with only the essential files.") 