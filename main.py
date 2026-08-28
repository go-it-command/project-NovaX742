"""CLI entry point for the personal assistant."""
"""
1. Імпортувати контактні функції з `contact_commands.py`.
2. Імпортувати нотаткові функції з `note_commands.py`.
3. Замінити `split()` у `parse_input` на `shlex.split()`; якщо криві лапки,
   показати помилку і продовжити цикл.
4. У наявному `match` залишити всі основні й тегові команди.
5. У `case _` викликати `suggest_command(command)`; якщо є результат, надрукувати
   `Unknown command. Did you mean: <command>?`, інакше `Invalid command.`.
6. Лишити `load_data()` до циклу та `save_data()` в `exit|close`.
7. Меню друкувати один раз на старті.
"""

import shlex

from contact_commands import (
    add_contact,
    birthdays,
    change_contact,
    delete_contact,
    find_contact,
)
from note_commands import (
    add_note,
    add_tag,
    change_note,
    delete_note,
    delete_tag,
    edit_tag,
    find_note,
    show_notes_by_tag,
    sort_notes_by_tags,
)
from command_suggester import suggest_command
from storage import load_data, save_data
    

def parse_input(user_input: str):
    """Return a lower-case command and whitespace-separated arguments.

    Use shlex.split to support quoted values and handle malformed quotes
    without closing the CLI.
    """
    try:
        parts = shlex.split(user_input)
    except ValueError:
        # Наприклад, незакриті лапки не повинні завершувати CLI.
        return None, []

    if not parts:
        return "", []

    command, *args = parts
    return command.lower(), args


def print_menu():
    """Виводить меню один раз під час запуску."""
    print("""
Available commands:
    add-contact <name> ...
    change-contact <id or query>
    find-contact <query>
    delete-contact <id or query>
    birthdays <days>

    add-note
    find-note <query>
    change-note <note_id>
    delete-note <note_id>

    add-tag <note_id> <tag>
    edit-tag <note_id> <old_tag> <new_tag>
    delete-tag <note_id> <tag>
    show-notes-by-tag <tag>
    sort-notes-by-tags

    exit / close
    """)


def greeting():
    return "How can I help you?"

    
def main():
    """Run the direct command loop until the user enters ``exit`` or ``close``."""
    contacts, notes = load_data()
    # print("Welcome to the assistant bot!")
    print("Welcome to the assistant bot!")
    print_menu()
    print(greeting())

    while True:
        # user_input = input("Enter a command: ").strip()

        try:
            user_input = input("Enter a command: ").strip()
        except (EOFError, KeyboardInterrupt):
            # Зберігаємо дані навіть при Ctrl+C.
            print("\nGood bye!")
            save_data(contacts, notes)
            break

        if not user_input:
            continue

        command, args = parse_input(user_input)

        if command is None:
            print("Invalid command syntax. Check quotation marks.")
            continue

        match command:
            case "close" | "exit":
                # Зберігаємо обидві книги перед завершенням програми.
                save_data(contacts, notes)
                print("Good bye!")
                break

            # Команди контактів.
            case "add-contact":
                print(add_contact(contacts))
            case "change-contact":
                print(change_contact(args, contacts))
            case "find-contact":
                print(find_contact(args, contacts))
            case "delete-contact":
                print(delete_contact(args, contacts))
            case "birthdays":
                print(birthdays(args, contacts))

            # Основні команди нотаток.
            case "add-note":
                print(add_note(notes))
            case "find-note":
                print(find_note(args, notes))
            case "change-note":
                print(change_note(args, notes))
            case "delete-note":
                print(delete_note(args, notes))

            # Optional commands.
            case "add-tag":
                print(add_tag(args, notes))
            case "edit-tag":
                print(edit_tag(args, notes))
            case "delete-tag":
                print(delete_tag(args, notes))
            case "show-notes-by-tag":
                print(show_notes_by_tag(args, notes))
            case "sort-notes-by-tags":
                print(sort_notes_by_tags(notes))

            case _:
                # print("Invalid command.")
                suggestion = suggest_command(command)
                if suggestion:
                    print(f"Unknown command. Did you mean: {suggestion}?")
                else:
                    print("Invalid command.")


if __name__ == "__main__":
    main()
