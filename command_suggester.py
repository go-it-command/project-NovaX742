from difflib import get_close_matches


COMMANDS = [
    "close",
    "exit",
    "add-contact",
    "change-contact",
    "find-contact",
    "delete-contact",
    "birthdays",
    "add-note",
    "find-note",
    "change-note",
    "delete-note",
    "add-tag",
    "edit-tag",
    "delete-tag",
    "show-notes-by-tag",
    "sort-notes-by-tags",
]


def suggest_command(text: str):
    normalized_text = text.strip().lower()

    if not normalized_text:
        return None

    matches = get_close_matches(
        normalized_text,
        COMMANDS,
        n=1,
        cutoff=0.6,
    )

    return matches[0] if matches else None