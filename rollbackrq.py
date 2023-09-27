
# Broken right now. Need to fix.

"""
rollbackrq.py

This script is designed to roll back files to their most recent backup version. 
It specifically targets a certain type of file (e.g., .txt, .py, .html) and replaces the current version of that file with its most recent backup.

The script performs the following operations:
1. Checks if the rollback directory exists.
2. Retrieves a list of all backup files for the specified file type.
3. Sorts the backups by creation time (newest first).
4. Creates a special backup of the current state before rolling back.
5. Replaces the current file with the newest backup.

The script uses the Python built-in modules os, sys, shutil, and the datetime module from the datetime package.

Functions:
rollback(file_type): Rolls back to the most recent backup of a specific file type.
create_special_backup(file_type): Creates a special backup of the current state.

Author: Your Name
Date: Current Date
"""

import os
import sys
from datetime import datetime
import shutil

# Function to roll back to the most recent backup of a specific file type
def rollback(file_type):
    """
    This function rolls back to the most recent backup of a specific file type.
    
    Parameters:
    file_type (str): The type of the file to be rolled back.
    """
    # Ensure the rollback directory exists
    if not os.path.exists('rollback'):
        print("No rollback directory found.")
        return

    # Get a list of all backup files for the specified file type
    backups = [f for f in os.listdir('rollback') if f.endswith(f'_backup.{file_type}')]

    # If no backups are found, notify the user and return
    if not backups:
        print(f"No backups found for file type: {file_type}")
        return

    # Sort the backups by creation time (newest first)
    backups.sort(key=lambda f: os.path.getmtime(f'rollback/{f}'), reverse=True)

    # Get the newest backup file
    newest_backup = backups[0]

    # Create a special backup of the current state
    create_special_backup(file_type)

    # Replace the current file with the newest backup
    shutil.copy2(f'rollback/{newest_backup}', f'{file_type}')

    # Notify the user that the rollback was successful
    print(f"Rolled back {file_type} to the most recent backup.")

# Function to create a special backup of the current state
def create_special_backup(file_type):
    """
    This function creates a special backup of the current state.
    
    Parameters:
    file_type (str): The type of the file to be backed up.
    """
    # Check if the file exists
    if os.path.isfile(file_type):
        # Get the current time and format it as a string
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        # Append the timestamp to the filename to create the backup filename
        backup_filename = f'{file_type}_special_backup_{timestamp}.txt'

        # Copy the file to create the backup in the rollback directory
        shutil.copy2(file_type, f'rollback/{backup_filename}')

        # Notify the user that the backup was created
        print(f"Special backup `rollback/{backup_filename}` created.")
    else:
        print(f"No existing {file_type} file found. A new one will be created.")

# Get the file types from the command line arguments
file_types = sys.argv[1:]

# Roll back each file type
for file_type in file_types:
    rollback(file_type)
