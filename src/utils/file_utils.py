import os
import zipfile
from datetime import datetime
from pathlib import Path

def get_latest_files(directory: str, file_types: list = ['.webm', '.zip']) -> dict:
    """Get the latest files of specified types from a directory."""
    latest_files = {}
    
    if not os.path.exists(directory):
        return latest_files
        
    for file_type in file_types:
        matching_files = []
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith(file_type):
                    full_path = os.path.join(root, file)
                    matching_files.append((full_path, os.path.getmtime(full_path)))
        
        if matching_files:
            # Get the most recently modified file
            latest_file = max(matching_files, key=lambda x: x[1])[0]
            latest_files[file_type] = latest_file
            
    return latest_files
