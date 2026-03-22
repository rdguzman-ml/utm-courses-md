"""
.add_courses/add_courses.py
[...]
"""

# Local imports
from .web_scraper import scrape_web_data
from .data_processing import format_data, create_md_file


def add_courses(vault_path: str) -> None:
    while True:
        course_code = input('Enter course code: ').strip().upper()
        if course_code == 'E':
            break

        course = scrape_web_data(course_code)
        md_file_text = format_data(course)

        create_md_file(course_code, md_file_text, vault_path)
        print('Course saved successfully...\n')
