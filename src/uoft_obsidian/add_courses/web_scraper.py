"""
.add_courses/web_scraper.py
[...]
"""

# Third-party imports
import requests
from bs4 import BeautifulSoup

# Local imports
from .validation import is_valid_course_code, get_course_pattern, get_department


def get_url(department: str, course_code: str) -> str:
    return f'https://{department}.calendar.utoronto.ca/course/{course_code}'


# Modified from original (no longer supports department of engineering)
def get_response(course: dict) -> requests.Response:
    if (response := requests.get(course['URL'])).status_code != 200:
        raise ConnectionError('ERROR: Unable connect to utoronto website')

    return response


def get_name(soup: BeautifulSoup, department: str) -> str:
    def get_delimiter(department_: str) -> str:
        if department_  == 'utm':
            return ' • '
        return ': '

    return soup.find('h1', class_='page-title').text.split(get_delimiter(department))[1]


def get_categories(soup: BeautifulSoup) -> list:
    return soup.find_all('label', class_='field__label')


def get_information(soup: BeautifulSoup) -> list:
    return soup.find_all('div', class_='w3-bar-item field__item')


def get_description(soup: BeautifulSoup) -> str:
    return soup.find_all('div', class_='w3-row field field--name-body field--type-text-with-summary field--label-hidden w3-bar-item field__item')[-2].text


def update_course_info(course: dict, categories: list, information: list) -> None:
    categories_text = []
    information_text = []

    for category in categories:
        categories_text.append(category.text.replace('\n', ''))

    for information in information:
        information_text.append(information.text.replace('\n', ''))

    # For multiple modes of delivery
    if len(categories_text) < len(information_text):
        while len(information_text) > len(categories_text):
            information_text[-3] = ' / '.join([information_text[-3], information_text[-2]])
            del information_text[-2]

    for category, information in zip(categories_text, information_text):
        course[category] = information


def scrape_web_data(course_code: str) -> dict:
    if not is_valid_course_code(course_code, get_course_pattern()):
        return {'INVALID': 'COURSE_CODE'}  # Deal with this in add_courses.py (while loop until valid)

    department = get_department(course_code)

    # course['URL'] must be initialized before get_response() is called
    course = {'Code': course_code, 'URL': get_url(department, course_code)}

    response = get_response(course)
    soup = BeautifulSoup(response.text, 'html.parser')

    course['Name'] = get_name(soup, department)

    categories = get_categories(soup)
    information = get_information(soup)

    # For UTSG courses with no header for description
    if str(course['Code'])[-1] == '1':
        course['Hours'] = information[0].text.replace('\n', '')
        del categories[0], information[0]

        course['Description'] = get_description(soup)

    update_course_info(course, categories, information)

    return course
