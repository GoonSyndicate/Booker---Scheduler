"""
This script is a utility tool designed to consolidate multiple code files into a single 'master.txt' file, 
making it easier to perform modifications across these files. 

The script performs the following operations:
1. Creates a timestamped backup of the existing 'master.txt' file for potential rollback.
2. Sequentially loads and processes four specific files: 'index.html', 'styles.css', 'script.js', and 'eventdb.py'. 
   For each file, the script:
   - Prints a terminal message indicating the loading process.
   - Identifies the corresponding section in the 'master.txt' file using specific tags.
   - Appends the content of the loaded file to the 'master.txt' file, replacing the identified section.
   - Ensures the correct tags are present after appending.
   - Prints a terminal message confirming successful loading and appending.
3. Utilizes the 'os', 're', and 'datetime' modules for file-path manipulations, regex operations, and timestamp operations respectively.

The script includes three main functions:
- 'load_file(filename)': Checks if the provided file exists, loads it if it does, and returns its content.
- 'update_master_file(master_filename, filename, content)': Updates the master file with the content of the provided file.
- 'create_new_master(master_filename)': Creates a new timestamped master file.

The script iterates over a list of files, loads each file, and updates the master file with its content. After all files have been processed, a new timestamped master file is created.

This tool can be particularly beneficial for ADHD users by automating the consolidation process, reducing cognitive load and potential for distraction.
"""

import os
from datetime import datetime
import shutil
import re

# Function to create a backup of a file
def create_backup(master_filename):
    # Check if the file exists
    if os.path.isfile(master_filename):
        # Get the current time and format it as a string
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        # Append the timestamp to the filename to create the backup filename
        backup_filename = f'{master_filename}_backup_{timestamp}.txt'

        # Ensure the rollback directory exists
        if not os.path.exists('rollback'):
            os.makedirs('rollback')

        # Copy the file to create the backup in the rollback directory
        shutil.copy2(master_filename, f'rollback/{backup_filename}')

        # Notify the user that the backup was created
        print(f"Backup `rollback/{backup_filename}` created.")
    else:
        print("No existing master file found. A new one will be created.")

# Function to load a provided file
def load_file(filename):
    if not os.path.isfile(filename):
        print(f"File {filename} does not exist.")
        return None

    with open(filename, 'r') as file:
        content = file.read()
        print(f"Loading `{filename}`...")
    
    return content

# Function to update a master file with the content of a provided file
def update_master_file(master_filename, filename, content):
    with open(master_filename, 'r+') as master_file:
        master_content = master_file.read()

        start_tag = f'<!-- {filename} -->'
        end_tag = f'<!-- /{filename} -->'

        tags_exist = start_tag in master_content and end_tag in master_content

        if not tags_exist:
            master_content += f'\n{start_tag}\n{end_tag}\n'

        file_block_pattern = f'{start_tag}.*{end_tag}'
        new_file_block = f'{start_tag}\n{content}\n{end_tag}'

        new_content = re.sub(file_block_pattern, new_file_block, master_content, flags=re.DOTALL)
        
        master_file.seek(0)
        master_file.write(new_content)
        master_file.truncate()

        print(f"`{filename}` successfully loaded!")

# Name of the master file
master_filename = 'master.txt'

# List of files to load
files = ['index.html', 'styles.css', 'script.js', 'eventdb.py']

# Create a backup of the existing master file (if it exists)
create_backup(master_filename)

# Iterate over the list of files
for filename in files:
    content = load_file(filename)
    if content is not None:
        update_master_file(master_filename, filename, content)
