"""
uoft_obsidian/main.py
[...]
"""

# Local imports
from vault_functions import read_saved_vault_path, get_vault_basename,change_vaults, create_new_vault, change_vault_path, print_vault
from add_courses import add_courses
from calculators import display_credit_count, display_hours


def start_menu(vault_path: str) -> int:
    menu_options = [
        'Add Courses',
        'Calculate Credits',
        'Calculate Hours',
        'Change Vaults',
        'Create New Vault',
        'Print Courses',
        'Exit',
    ]

    if get_vault_basename(vault_path) == 'None':
        menu_options.remove('Add Courses')
        menu_options.remove('Calculate Credits')
        menu_options.remove('Calculate Hours')

    while True:
        for i in range(len(menu_options)):
            print(f'{i+1}. {menu_options[i]}')

        try:
            user_choice = int(input())

        except ValueError:
            print('Please enter an integer')
            continue

        if not(1 <= user_choice <= len(menu_options)):
            print('Please enter a number between 1 and 3')
            continue

        if get_vault_basename(vault_path) == 'None':
            user_choice += 3

        return user_choice


def main():
    while True:
        vault_path = read_saved_vault_path()
        print(f'Current Vault: {get_vault_basename(vault_path)}')

        match start_menu(vault_path):
            case 1:
                add_courses(vault_path)
            case 2:
                display_credit_count(vault_path)
            case 3:
                display_hours(vault_path)
            case 4:
                change_vaults(vault_path)
            case 5:
                create_new_vault(change_vault_path(vault_path))
            case 6:
                print_vault(vault_path)
            case _:
                break

        print()


if __name__ == '__main__':
    main()
