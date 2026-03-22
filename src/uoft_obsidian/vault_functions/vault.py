"""
.vault_functions/vault.py
[...]
"""

# Standard imports
import json
import os
import re

def initialize_json(json_file_name: str) -> None:
    """
    Initialize .json file with an Obsidian path to a non-existent placeholder directory called 'None'.
    :param json_file_name: The name of the .json file to initialize (called 'vault_path.json').
    :return: None
    """
    with open(json_file_name, 'w') as file:
        starting_path = f'{get_obsidian_path()}/None'
        json.dump({'vault_path': starting_path}, file)


def read_saved_vault_path() -> str:
    file_path = 'vault_path.json'

    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        initialize_json(file_path)

    with open(file_path, 'r') as file:
        data = json.load(file)

    if not os.path.exists(data['vault_path']):
        data['vault_path'] = f"{os.path.dirname(data['vault_path'])}/None"

    return data['vault_path']


def get_vault_basename(vault_path: str) -> str:
    return os.path.basename(vault_path)


def get_obsidian_path() -> str:
    while True:
        obsidian_path = input('Enter path to Obsidian vault_functions directory: ').strip()

        if os.path.exists(obsidian_path):
            return obsidian_path


def get_vault_name() -> str:
    while True:
        vault_name = input('Enter vault name: ').strip()

        if vault_name == 'None':
            print('ERROR: This vault name has been reserved for special use.\nPlease choose a different vault name.\n')
            continue

        return vault_name


def save_vault_path(vault_path: str) -> None:
    data = {'vault_path': vault_path}

    with open('vault_path.json', 'w') as file:
        json.dump(data, file, indent=4)

def create_new_vault(vault_path: str) -> None:
    directories = ['1st Year', '2nd Year', '3rd Year', '4th Year']
    sub_directories = ['Both Terms', 'Fall Term', 'Winter Term']

    for directory in directories:
        for sub_directory in sub_directories:
            os.makedirs(os.path.join(vault_path, directory, sub_directory))

    save_vault_path(vault_path)



def change_vault_path(current_path: str) -> str:
    return f'{os.path.dirname(current_path)}/{get_vault_name()}'


def is_new_vault() -> bool:
    prompt_response = input('Would you like to create a new vault? (y/n) ')
    return prompt_response.lower() == 'y'


def change_vaults(current_path: str) -> None:
    while True:
        new_path = change_vault_path(current_path)

        if os.path.exists(new_path):
            break

        elif is_new_vault():
            create_new_vault(new_path)
            break

    save_vault_path(new_path)


def extract_course_name(md_file_path: str) -> str:
    """Extracts the course name from a .md file by searching the Course Information table."""
    with open(md_file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

        for line in lines:
            match = re.match(r"^\| \[.*?\]\(.*?\) \| (.+?) \|",
                             line.strip())  # Extract second column
            if match:
                return match.group(1).strip()

    return "Course name not found"


def print_vault(vault_path: str) -> None:
    """Prints the file name (without extension) and the extracted course name from each .md file."""
    for root, _, files in os.walk(vault_path):
        if 'Extra' in root or 'Not Offered' in root:
            continue

        for file in files:
            if file.endswith(".md") and ' - R' not in file:
                name = os.path.splitext(file)[0]
                if name.isupper():  # Only process files with all-uppercase names
                    file_path = os.path.join(root, file)
                    course_name = extract_course_name(file_path)
                    print(f"{name}: {course_name}")