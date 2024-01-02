import os

# Set the directory where your python files are stored
py_files_dir = '.'

# List of python files to be concatenated
py_files = ['app.py', 'auth.py', 'forms.py', 'main.py', 'models.py', 'utils.py']

output_file = 'all_python_files.txt'

# Concatenate the content of each Python file into a single string
all_content = ''
for py_file in py_files:
    with open(os.path.join(py_files_dir, py_file), 'r', encoding='utf-8') as file:
        all_content += file.read() + '\n\n'  # Add some space between files

# Write the concatenated content to the output file
with open(output_file, 'w', encoding='utf-8') as file:
    file.write(all_content)

print(f"All Python files have been concatenated into {output_file}")
