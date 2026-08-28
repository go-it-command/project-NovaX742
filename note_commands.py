import uuid
from models import Note


def add_note(notes):
    """Creates a note with a unique UUID and text from user input."""
    while True:
        text = input("Note text: ").strip()
        if not text:
            print("Note text cannot be empty. Please try again.")
            continue

        try:
            note_id = str(uuid.uuid4())
            note = Note(note_id, text)
            notes.add(note)
            return f"Note added: {note}"
        except (ValueError, KeyError) as e:
            print(f"Error: {e}. Please try again.")


def find_note(args, notes):
    """Searches for notes based on a text query."""
    if not args:
        return "Usage: find-note <query>"

    query = " ".join(args)
    found_notes = notes.search(query)

    if not found_notes:
        return "No notes found."

    return "\n".join(str(note) for note in found_notes)


def change_note(args, notes):
    """Edits the text of an existing note by its UUID."""
    if not args:
        return "Usage: change-note <note_id>"

    note_id = args[0]
    note = notes.find_by_id(note_id)

    if not note:
        return "Note not found."

    while True:
        new_text = input("New note text: ").strip()
        if not new_text:
            print("Note text cannot be empty. Please try again.")
            continue

        try:
            note.edit_text(new_text)
            break
        except ValueError as e:
            print(f"Error: {e}. Please try again.")

    return f"Note updated: {note}"


def delete_note(args, notes):
    """Deletes a note by its UUID after user confirmation."""
    if not args:
        return "Usage: delete-note <note_id>"

    note_id = args[0]
    note = notes.find_by_id(note_id)

    if not note:
        return "Note not found."

    print(f"Found note: {note}")
    confirm = input("Are you sure? (yes/no): ").strip().lower()

    if confirm == "yes":
        try:
            notes.delete(note_id)
            return "Note deleted."
        except (ValueError, KeyError) as e:
            return str(e)

    return "Deletion cancelled."


def add_tag(args, notes):
    """Adds a tag to a note (add-tag <note_id> <tag>)."""
    if len(args) != 2:
        return "Usage: add-tag <note_id> <tag>"

    note_id, tag = args[0], args[1]
    note = notes.find_by_id(note_id)

    if not note:
        return "Note not found."

    try:
        note.add_tag(tag)
        return f"Updated note: {note}"
    except (ValueError, KeyError) as e:
        return str(e)


def edit_tag(args, notes):
    """Edits a tag on a note (edit-tag <note_id> <old_tag> <new_tag>)."""
    if len(args) != 3:
        return "Usage: edit-tag <note_id> <old_tag> <new_tag>"

    note_id, old_tag, new_tag = args[0], args[1], args[2]
    note = notes.find_by_id(note_id)

    if not note:
        return "Note not found."

    try:
        note.edit_tag(old_tag, new_tag)
        return f"Updated note: {note}"
    except (ValueError, KeyError) as e:
        return str(e)


def delete_tag(args, notes):
    """Deletes a tag from a note after confirmation (delete-tag <note_id> <tag>)."""
    if len(args) != 2:
        return "Usage: delete-tag <note_id> <tag>"

    note_id, tag = args[0], args[1]
    note = notes.find_by_id(note_id)

    if not note:
        return "Note not found."

    print(f"Found note: {note}")
    confirm = input("Are you sure? (yes/no): ").strip().lower()

    if confirm == "yes":
        try:
            note.delete_tag(tag)
            return f"Updated note: {note}"
        except (ValueError, KeyError) as e:
            return str(e)

    return "Deletion cancelled."


def show_notes_by_tag(args, notes):
    """Searches for notes by tag (show-notes-by-tag <tag>)."""
    if not args:
        return "Usage: show-notes-by-tag <tag>"

    tag = args[0]
    found_notes = notes.search_by_tag(tag)

    if not found_notes:
        return "No notes found."

    return "\n".join(str(note) for note in found_notes)


def sort_notes_by_tags(notes):
    """Sorts notes by their tags (sort-notes-by-tags)."""
    sorted_notes = notes.sort_by_tags()

    if not sorted_notes:
        return "No notes found."

    return "\n".join(str(note) for note in sorted_notes)
