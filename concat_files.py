import os

# Function to create a boxed delimiter for each file
def create_boxed_delimiter(file_name):
    top_bottom_border = "#" * (len(file_name) + 10)
    return f"\n\n{top_bottom_border}\n#    {file_name}    #\n{top_bottom_border}\n\n"

# Set the directories for static, templates, and python files
static_dir = 'static'
templates_dir = 'templates'
py_files_dir = '.'

# List of files to be concatenated from each directory
static_files = [
    'css/businessinfo.css',
    'css/calendar.css',
    'css/dashboard.css',
    'css/login.css',
    'css/logout.css',
    'css/signup.css',
    'css/styles.css',
    'js/script.js',
    'favicon.ico'
]

template_files = [
    'businessinfo.html',
    'calendar.html',
    'edit_reservation.html',
    'help_resources.html',
    'index.html',
    'login.html',
    'logout.html',
    'make_reservation.html',
    'online_bookings.html',
    'reports.html',
    'reviews.html',
    'setup_business.html',
    'setup_products.html',
    'signup.html',
    'userinfo.html',
    'view_reservation.html'
]

py_files = [
    'app.py',
    'auth.py',
    'extensions.py',
    'forms.py',
    'main.py',
    'models.py',
    'run.py',
    'utils.py'
]

output_file = 'all_files_concatenated.txt'

# Function to concatenate files from a given directory and list
def concatenate_files(directory, file_list):
    all_content = ''
    for file in file_list:
        delimiter = create_boxed_delimiter(file)
        with open(os.path.join(directory, file), 'r', encoding='utf-8') as f:
            all_content += delimiter + f.read() + '\n\n'
    return all_content

# Concatenate the content of each file type into a single string
all_content = ''
all_content += concatenate_files(static_dir, static_files)
all_content += concatenate_files(templates_dir, template_files)
all_content += concatenate_files(py_files_dir, py_files)

# Write the concatenated content to the output file
with open(output_file, 'w', encoding='utf-8') as file:
    file.write(all_content)

print(f"All files have been concatenated into {output_file}")
