# .add_courses/__init__.py
from .add_courses import add_courses
from .data_processing import format_data, create_md_file
from .validation import is_valid_course_code, get_course_pattern, get_department, is_irrelevant
from .web_scraper import scrape_web_data

__all__ = [
    'add_courses',
    'format_data',
    'create_md_file',
    'is_valid_course_code',
    'get_course_pattern',
    'get_department',
    'is_irrelevant',
    'scrape_web_data',
    ]