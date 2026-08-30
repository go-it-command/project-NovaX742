"""CLI entry point for the personal assistant."""

import shlex

from contact_commands import (
    add_contact,
    birthdays,
    change_contact,
    delete_contact,
    find_contact,
    show_all_contacts,
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


def parse_input(user_input: str) -> tuple[str | None, list[str]]:
    """Return a lower-case command and whitespace-separated arguments.

    Use shlex.split to support quoted values and handle malformed quotes
    without closing the CLI.
    """
    try:
        parts = shlex.split(user_input)
    except ValueError:
        return None, []

    if not parts:
        return "", []

    command, *args = parts
    return command.lower(), args


def print_menu() -> None:
    """Виводить меню один раз під час запуску."""
    print("""
Available commands:
    add-contact <name> ...
    change-contact <id or query>
    find-contact <query>
    show-all-contact
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


def greeting() -> str:
    """Return a short greeting shown at application startup."""
    return "How can I help you?"


def main() -> None:
    """Run the direct command loop until the
    user enters ``exit`` or ``close``."""
    contacts, notes = load_data()
    print("Welcome to the assistant bot!")
    print_menu()
    print(greeting())

    while True:
        try:
            user_input = input("Enter a command: ").strip()
        except (EOFError, KeyboardInterrupt):
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
                save_data(contacts, notes)
                print("Good bye!")
                break

            case "add-contact":
                print(add_contact(contacts))
            case "change-contact":
                print(change_contact(args, contacts))
            case "find-contact":
                print(find_contact(args, contacts))
            case "show-all-contact":
                print(show_all_contacts(contacts))
            case "delete-contact":
                print(delete_contact(args, contacts))
            case "birthdays":
                print(birthdays(args, contacts))

            case "add-note":
                print(add_note(notes))
            case "find-note":
                print(find_note(args, notes))
            case "change-note":
                print(change_note(args, notes))
            case "delete-note":
                print(delete_note(args, notes))

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
                suggestion = suggest_command(command)
                if suggestion:
                    print(f"Unknown command. Did you mean: {suggestion}?")
                else:
                    print("Invalid command.")


if __name__ == "__main__":
    main()
