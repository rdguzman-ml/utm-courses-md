"""
.calculators/credit_calculator.py
[...]
"""

# Standard imports
import os


def calculate_credits(vault_path: str) -> float:
    credit_count = 0.0

    for root, dirs, files in os.walk(vault_path):
        if os.path.basename(root) in ['Extra', 'Not Offered']:
            continue

        for file in files:

            if file.endswith('Y5.md') or file.endswith('Y1.md'):
                credit_count += 1

            elif file.endswith('H5.md') or file.endswith('H1.md'):
                credit_count += 0.5

    return credit_count


def display_credit_count(vault_path: str) -> None:
    credit_count = calculate_credits(vault_path)
    print(f'Number of credits: {credit_count}')
