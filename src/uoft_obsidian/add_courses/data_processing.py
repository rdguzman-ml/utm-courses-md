"""
.add_courses/data_processing.py
[...]
"""

# Standard imports
import os
import re

# Local imports
from .validation import is_irrelevant, get_course_pattern


def md_link_format_courses(course: dict) -> None:
    def replace(match):
        course_code = match.group(0)
        return f'[{course_code}]({course_code}.md)'

    for category, information in course.items():
        if is_irrelevant(category):
            continue

        course[category] = re.sub(get_course_pattern(), replace, information)


def get_max_length(course: dict) -> int:
    max_length = 0

    for information in course.values():
        if len(information) > max_length:
            max_length = len(information)

    return max_length


def format_data(course: dict) -> str:
    md_link_format_courses(course)

    # +4 to account for brackets [] and ()
    dashes_1 = '-' * (len(course['Code']) + len(course['URL']) + 4)

    max_length = get_max_length(course)
    dashes_2 = '-' * max_length

    title_white_space = ' ' * (len(dashes_2) - len(course['Name']))

    md_formatted_course = f'''
### Course Information
| [{course['Code']}]({course['URL']}) | {course['Name']}{title_white_space} |
| {dashes_1} | {dashes_2} |
'''

    for category, information in course.items():
        if is_irrelevant(category):
            continue

        category_white_space = ' ' * (len(dashes_1) - len(category))
        information_white_space = ' ' * (max_length - len(information))

        md_formatted_course += f'| {category}{category_white_space} | {information}{information_white_space} |\n'

    return md_formatted_course


# Remove weird invisible chars in HTML.text
def remove_unsupported_chars(text: str) -> str:
    return text.encode('ascii', 'ignore').decode('ascii')


def create_md_file(file_name: str, contents: str, directory: str) -> None:
    file_path = os.path.join(directory, f'{file_name}.md')

    with open(file_path, 'w') as file:
        file.write(remove_unsupported_chars(contents))
