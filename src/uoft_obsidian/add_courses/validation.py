"""
.add_courses/validation.py
[...]
"""

# Standard imports
import re


def is_valid_course_code(course_code: str, course_pattern: str) -> bool:
    return re.search(course_pattern, course_code) is not None


def get_course_pattern() -> str:
    artsci_utm_pattern = r'[A-Z]{3}\d{3}(H|Y)(1|5)'
    # Add additional patterns for other departments as needed
    ...

    return artsci_utm_pattern


def get_department(course_code: str) -> str:
    match course_code[-1]:
        case '1':
            return 'artsci'
        case '5':
            return 'utm'
        case _:
            # Add additional department codes as needed
            ...


# Skip certain categories to avoid duplicates when formatting md file
def is_irrelevant(category: str) -> bool:
    return category in ('Code', 'URL', 'Name')
