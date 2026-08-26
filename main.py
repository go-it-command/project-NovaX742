"""CLI entry point for the personal assistant."""

from commands import (
    add_contact,
    add_note,
    add_tag,
    birthdays,
    change_contact,
    change_note,
    delete_contact,
    delete_note,
    delete_tag,
    edit_tag,
    find_contact,
    find_note,
    greeting,
    show_notes_by_tag,
    sort_notes_by_tags,
)
from storage import load_data, save_data


def parse_input(user_input: str):
    """Return a lower-case command and whitespace-separated arguments.

    TODO: Use shlex.split to support quoted values and handle malformed quotes
    without closing the CLI.
    """
    command, *args = user_input.split()
    return command.lower(), args


def main():
    """Run the direct command loop until the user enters ``exit`` or ``close``."""
    contacts, notes = load_data()
    print("Welcome to the assistant bot!")
    print(greeting())

    while True:
        user_input = input("Enter a command: ").strip()
        if not user_input:
            continue

        command, args = parse_input(user_input)

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
            # Optional commands for the additional tag requirement.
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
                print("Invalid command.")


if __name__ == "__main__":
    main()
