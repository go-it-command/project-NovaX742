"""User scenarios for the CLI.

TODO: Each command must catch/translate expected validation and not-found errors
into readable messages; unexpected errors must not be hidden.
"""


def greeting():
    # TODO: Return a compact command menu shown at application start.
    pass


def add_contact(contacts):
    """Interactively create one contact with all supported fields."""
    # TODO: Prompt for name (required), phone, email, address and birthday.
    # Allow skipping optional values; re-prompt only an invalid field; generate
    # a UUID, construct Contact and add it to AddressBook.
    pass


def change_contact(args, contacts):
    """Find a contact, let the user select a field, then change that field."""
    # TODO: Search by id/query; if multiple matches, display ids and ask the
    # user to choose. Prompt for name/phone/email/address/birthday and use the
    # corresponding Contact setter; set_phone replaces the current number.
    pass


def find_contact(args, contacts):
    """Search contacts using one query across every searchable field."""
    # TODO: Call AddressBook.search and format all matches with their ids.
    pass


def delete_contact(args, contacts):
    """Find by any field, select one result and confirm deletion."""
    # TODO: Search, handle zero/one/many matches, ask confirmation and delete
    # only the selected contact id. Delete only if the user answers "yes".
    pass


def birthdays(args, contacts):
    """Show upcoming birthdays for the specified number of days."""
    # TODO: Parse a non-negative integer horizon and format the result.
    pass


def add_note(notes):
    """Interactively add one standalone text note."""
    # TODO: Prompt for non-empty text, generate UUID, construct Note and add it.
    pass


def find_note(args, notes):
    """Search standalone notes by text."""
    # TODO: Call NotesBook.search and format matching notes with ids and tags.
    pass


def change_note(args, notes):
    """Edit standalone note text by note id."""
    # TODO: Find note, prompt for replacement text, call Note.edit_text.
    pass


def delete_note(args, notes):
    """Confirm and delete a standalone note by note id."""
    # TODO: Show the selected note, ask "Are you sure? (yes/no)", then delete
    # it only after "yes".
    pass


# Optional functionality: tags (additional project requirements).
def add_tag(args, notes):
    """CLI contract: ``add-tag <note_id> <tag>``."""
    # TODO: Find note and call Note.add_tag.
    pass


def edit_tag(args, notes):
    """CLI contract: ``edit-tag <note_id> <old_tag> <new_tag>``."""
    # TODO: Find note and call Note.edit_tag.
    pass


def delete_tag(args, notes):
    """CLI contract: ``delete-tag <note_id> <tag>``."""
    # TODO: Show the selected tag, ask "Are you sure? (yes/no)", then call
    # Note.delete_tag only after "yes".
    pass


def show_notes_by_tag(args, notes):
    """CLI contract: ``show-notes-by-tag <tag>``."""
    # TODO: Search NotesBook by tag and format matching notes.
    pass


def sort_notes_by_tags(notes):
    """CLI contract: ``sort-notes-by-tags``."""
    # TODO: Format NotesBook.sort_by_tags() output.
    pass
