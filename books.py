"""Repositories for contacts and standalone notes, both keyed by stable ids."""

from collections import UserDict

from upcoming_birthdays import get_upcoming_birthdays


class AddressBook(UserDict):
    """Store ``Contact`` objects as ``{contact_id: contact}``."""

    def add(self, contact):
        # TODO: Reject a duplicate normalized contact name, then store contact.
        pass

    def find_by_id(self, contact_id: str):
        # TODO: Return a Contact by id, or None.
        pass

    def search(self, query: str):
        # TODO: Return every partial, case-insensitive match across name,
        # phone, email, address and birthday.
        pass

    def delete(self, contact_id: str):
        # TODO: Delete a Contact by id or report it missing. Confirmation is
        # performed by the user-facing command before this method is called.
        pass

    def get_upcoming_birthdays(self, days: int):
        # TODO: Validate days and delegate the calculation to the helper.
        pass


class NotesBook(UserDict):
    """Store standalone ``Note`` objects as ``{note_id: note}``."""

    def add(self, note):
        # TODO: Reject a duplicate id and store note.
        pass

    def find_by_id(self, note_id: str):
        # TODO: Return a Note by id, or None.
        pass

    def search(self, query: str):
        # TODO: Return every note whose text partially matches query.
        pass

    def search_by_tag(self, tag: str):
        # TODO: Normalize tag and return every note that contains it.
        pass

    def sort_by_tags(self):
        # TODO: Return all notes ordered by tags, with untagged notes last;
        # use text or id as a deterministic tie-breaker.
        pass

    def delete(self, note_id: str):
        # TODO: Delete a Note by id or report it missing. Confirmation is
        # performed by the user-facing command before this method is called.
        pass
