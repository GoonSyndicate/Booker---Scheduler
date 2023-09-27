"""
pusher.py

This script is designed to manage the content of multiple files using a master file. 
The master file contains the content for each file, enclosed in unique start and end tags.

The script performs the following operations:
1. Load the master file.
2. Extract the content for each file from the master file.
3. Create a backup of each file before updating it.
4. Update each file with its new content extracted from the master file.

The script uses the Python built-in modules os and re, and the datetime module from the datetime package.

Functions:
load_master_file(master_filename): Loads a master file and returns its content.
extract_content(master_content, filename): Extracts the content for a specific file from the master file.
create_backup(filename): Creates a backup of a specified file.
update_file(filename, content): Updates a specified file with new content.

Author: Your Name
Date: Current Date
"""

import os
import re
from datetime import datetime

# Function to load the master file
def load_master_file(master_filename):
    """
    This function loads a master file and returns its content.
    
    Parameters:
    master_filename (str): The name of the master file.

    Returns:
    str: The content of the master file if it exists, None otherwise.
    """
    # Check if the desired file exists
    if not os.path.isfile(master_filename):
        # Notify the user if the file wasn't found
        print(f"File {master_filename} does not exist.")
        return None

    # Load and read the file 
    with open(master_filename, 'r') as file:
        content = file.read()
        print(f"Loading `{master_filename}`...")
    
    # Return the file's content as a string
    return content

# Function to extract content for a specific file from the master file
def extract_content(master_content, filename):
    """
    This function extracts the content for a specific file from the master file.
    
    Parameters:
    master_content (str): The content of the master file.
    filename (str): The name of the file whose content is to be extracted.

    Returns:
    str: The content of the specified file if it exists in the master file, None otherwise.
    """
    # Create unique start and end tags for the current file's content 
    start_tag = f'<!-- {filename} -->'
    end_tag = f'<!-- /{filename} -->'

    # Create a regex pattern to match the entire block of this file's content in the master file
    file_block_pattern = f'{start_tag}(.*?){end_tag}'

    # Extract the block of this file's content from the master file
    file_block = re.search(file_block_pattern, master_content, flags=re.DOTALL)

    # If the block was found, return its content (without the tags)
    if file_block:
        return file_block.group(1).strip()

    # If the block wasn't found, notify the user and return None
    print(f"No content found for `{filename}` in the master file.")
    return None

# Function to create a backup of a file
def create_backup(filename):
    """
    This function creates a backup of a specified file.
    
    Parameters:
    filename (str): The name of the file to be backed up.
    """
    # Check if the file exists
    if not os.path.isfile(filename):
        print(f"File {filename} does not exist. No backup created.")
        return

    # Get the current time and format it as a string
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    # Append the timestamp to the filename to create the backup filename
    backup_filename = f'{filename}_backup_{timestamp}'

    # Ensure the rollback directory exists
    if not os.path.exists('rollback'):
        os.makedirs('rollback')

    # Copy the file to create the backup in the rollback directory
    os.system(f'copy {filename} rollback\{backup_filename}')

    # Notify the user that the backup was created
    print(f"Backup `rollback\{backup_filename}` created.")

# Function to update a file with new content
def update_file(filename, content):
    """
    This function updates a specified file with new content.
    
    Parameters:
    filename (str): The name of the file to be updated.
    content (str): The new content to be written to the file.
    """
    # Create a backup of the file before overwriting it
    create_backup(filename)

    # Open the file to write
    with open(filename, 'w') as file:
        # Write the new content to the file
        file.write(content)

        # Notify the user that the file was successfully updated
        print(f"`{filename}` successfully updated!")

# Name of the master file
master_filename = 'master.txt'

# List of files to update
files = ['index.html', 'styles.css', 'script.js', 'eventdb.py']

# Load the master file and return its content
master_content = load_master_file(master_filename)

# If the master file was successfully loaded (i.e. exists and read)
if master_content is not None:
    # Iterate over the list of files
    for filename in files:
        # Extract the content for this file from the master file
        content = extract_content(master_content, filename)

        # If content was found for this file, update the file with the new content
        if content is not None:
            update_file(filename, content)


import os
import re
from datetime import datetime

# Function to load the master file
def load_master_file(master_filename):
    """
    This function loads a master file and returns its content.
    
    Parameters:
    master_filename (str): The name of the master file.

    Returns:
    str: The content of the master file if it exists, None otherwise.
    """
    # Check if the desired file exists
    if not os.path.isfile(master_filename):
        # Notify the user if the file wasn't found
        print(f"File {master_filename} does not exist.")
        return None

    # Load and read the file 
    with open(master_filename, 'r') as file:
        content = file.read()
        print(f"Loading `{master_filename}`...")
    
    # Return the file's content as a string
    return content

# Function to extract content for a specific file from the master file
def extract_content(master_content, filename):
    """
    This function extracts the content for a specific file from the master file.
    
    Parameters:
    master_content (str): The content of the master file.
    filename (str): The name of the file whose content is to be extracted.

    Returns:
    str: The content of the specified file if it exists in the master file, None otherwise.
    """
    # Create unique start and end tags for the current file's content 
    start_tag = f'<!-- {filename} -->'
    end_tag = f'<!-- /{filename} -->'

    # Create a regex pattern to match the entire block of this file's content in the master file
    file_block_pattern = f'{start_tag}(.*?){end_tag}'

    # Extract the block of this file's content from the master file
    file_block = re.search(file_block_pattern, master_content, flags=re.DOTALL)

    # If the block was found, return its content (without the tags)
    if file_block:
        return file_block.group(1).strip()

    # If the block wasn't found, notify the user and return None
    print(f"No content found for `{filename}` in the master file.")
    return None

# Function to create a backup of a file
def create_backup(filename):
    """
    This function creates a backup of a specified file.
    
    Parameters:
    filename (str): The name of the file to be backed up.
    """
    # Check if the file exists
    if not os.path.isfile(filename):
        print(f"File {filename} does not exist. No backup created.")
        return

    # Get the current time and format it as a string
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    # Append the timestamp to the filename to create the backup filename
    backup_filename = f'{filename}_backup_{timestamp}'

    # Ensure the rollback directory exists
    if not os.path.exists('rollback'):
        os.makedirs('rollback')

    # Copy the file to create the backup in the rollback directory
    os.system(f'copy {filename} rollback\{backup_filename}')

    # Notify the user that the backup was created
    print(f"Backup `rollback\{backup_filename}` created.")

# Function to update a file with new content
def update_file(filename, content):
    """
    This function updates a specified file with new content.
    
    Parameters:
    filename (str): The name of the file to be updated.
    content (str): The new content to be written to the file.
    """
    # Create a backup of the file before overwriting it
    create_backup(filename)

    # Open the file to write
    with open(filename, 'w') as file:
        # Write the new content to the file
        file.write(content)

        # Notify the user that the file was successfully updated
        print(f"`{filename}` successfully updated!")

# Name of the master file
master_filename = 'master.txt'

# List of files to update
files = ['index.html', 'styles.css', 'script.js', 'eventdb.py']

# Load the master file and return its content
master_content = load_master_file(master_filename)

# If the master file was successfully loaded (i.e. exists and read)
if master_content is not None:
    # Iterate over the list of files
    for filename in files:
        # Extract the content for this file from the master file
        content = extract_content(master_content, filename)

        # If content was found for this file, update the file with the new content
        if content is not None:
            update_file(filename, content)
