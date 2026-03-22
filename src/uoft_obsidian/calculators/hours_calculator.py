"""
.calculators/hours_calculator.py
[...]
"""

# Standard imports
import os
import re


def extract_hours(file_path: str) -> float:
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

        # This is why we hate regex...           like seriously how tf do u even read that???
        match = re.findall(r'Hours\s*\|\s*(\d+\.?\d+?)[LSP](/(\d+\.?\d+?)[PST])?', content)

        if not match:
            return 0.0

        match = match[0]

        if match[1] == '':
            return float(match[0])

        return float(match[0]) + float(match[2])


def sum_term_hours(vault_path: str) -> float:
    term_hours = 0.0

    for file_name in os.listdir(vault_path):
        file_path = os.path.join(vault_path, file_name)
        term_hours += extract_hours(file_path)

    return term_hours


def sum_years_hours(vault_path: str) -> list:
    total_hours = []
    final_hours = [0, 0, 0]

    for sub_path in os.listdir(vault_path):
        if os.path.basename(sub_path) == '.DS_Store':
            continue

        total_hours.append(sum_term_hours(os.path.join(vault_path, sub_path)))

    if len(total_hours) == 3:
        split_share = total_hours[0] / 2

        total_hours[1] += split_share
        total_hours[2] += split_share

        del total_hours[0]

    final_hours[0] = total_hours[0]
    final_hours[1] = total_hours[1]

    return final_hours


def display_hours(vault_path: str) -> None:
    sub_paths = os.listdir(vault_path)
    sub_paths.sort()

    for path in sub_paths:
        if '.' in path or path in ['Extra', 'Not Offered']:
            continue

        current_path = os.path.join(vault_path, path)
        total_hours = sum_years_hours(current_path)

        print(f'''
{os.path.basename(current_path)}
Fall Term: {total_hours[0]} h
Winter Term: {total_hours[1]} h''')
