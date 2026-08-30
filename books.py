"""Repositories for contacts and standalone notes, both keyed by stable ids."""

from collections import UserDict

from upcoming_birthdays import get_upcoming_birthdays


def _as_text(value) -> str:
    """Return a plain string for a field object, a raw value or ``None``."""
    if value is None:
        return ""
    return str(getattr(value, "value", value) or "")


def _normalize_tag(tag) -> str:
    """Normalize a tag the same way ``Note`` does: no '#', lower-case, trimmed."""
    return _as_text(tag).strip().lstrip("#").strip().lower()


class AddressBook(UserDict):
    """Store ``Contact`` objects as ``{contact_id: contact}``."""

    def add(self, contact):
        """Store contact under its id.

        Ids are unique; names are not — two contacts may both be named
        "Олександр" as long as their UUIDs differ.
        """
        contact_id = _as_text(contact.id)
        if not contact_id:
            raise ValueError("Contact must have an id.")
        if contact_id in self.data:
            raise ValueError(f"Contact with id '{contact_id}' already exists.")

        self.data[contact_id] = contact
        return contact

    def find_by_id(self, contact_id: str):
        """Return a Contact by id, or None."""
        return self.data.get(contact_id)

    def search(self, query: str):
        """Return every partial, case-insensitive match across name,
        phone, email, address and birthday."""
        needle = _as_text(query).strip().lower()
        if not needle:
            return []

        return [
            contact
            for contact in self.data.values()
            if needle in self._haystack(contact)
        ]

    @staticmethod
    def _haystack(contact) -> str:
        """Flatten a contact into one lower-case string used for searching."""
        parts = [
            _as_text(contact.id),
            _as_text(contact.name),
            _as_text(contact.phone),
            _as_text(contact.email),
            _as_text(contact.address),
            _as_text(contact.birthday),
        ]

        return " ".join(part for part in parts if part).lower()

    def delete(self, contact_id: str):
        """Delete a Contact by id or report it missing. Confirmation is
        performed by the user-facing command before this method is called."""
        if contact_id not in self.data:
            raise KeyError(f"Contact with id '{contact_id}' was not found.")

        del self.data[contact_id]

    def get_upcoming_birthdays(self, days: int):
        """Validate days and delegate the calculation to the helper."""
        if isinstance(days, bool) or not isinstance(days, int):
            raise ValueError("Number of days must be an integer.")
        if days < 0:
            raise ValueError("Number of days must not be negative.")

        return get_upcoming_birthdays(self, days)


class NotesBook(UserDict):
    """Store standalone ``Note`` objects as ``{note_id: note}``."""

    def add(self, note):
        """Reject a duplicate id and store note."""
        note_id = _as_text(note.id)
        if note_id in self.data:
            raise ValueError(f"Note with id '{note_id}' already exists.")

        self.data[note_id] = note
        return note

    def find_by_id(self, note_id: str):
        """Return a Note by id, or None."""
        return self.data.get(note_id)

    def search(self, query: str):
        """Return every note whose text partially matches query."""
        needle = _as_text(query).strip().lower()
        if not needle:
            return []

        return [
            note
            for note in self.data.values()
            if needle in _as_text(note.text).lower()
        ]

    def search_by_tag(self, tag: str):
        """Normalize tag and return every note that contains it."""
        needle = _normalize_tag(tag)
        if not needle:
            return []

        return [
            note
            for note in self.data.values()
            if needle in self._tags(note)
        ]

    def sort_by_tags(self):
        """Return all notes ordered by tags, with untagged notes last;
        use text or id as a deterministic tie-breaker."""
        def sort_key(note):
            tags = self._tags(note)
            first_tag = min(tags) if tags else ""
            return (not tags, first_tag, _as_text(note.id))

        return sorted(self.data.values(), key=sort_key)

    @staticmethod
    def _tags(note) -> set:
        """Return the normalized, de-duplicated tags of a note."""
        raw = getattr(note, "tags", None) or []
        if isinstance(raw, str):
            raw = [raw]

        return {tag for tag in (_normalize_tag(item) for item in raw) if tag}

    def delete(self, note_id: str):
        """Delete a Note by id or report it missing. Confirmation is
        performed by the user-facing command before this method is called."""
        if note_id not in self.data:
            raise KeyError(f"Note with id '{note_id}' was not found.")

        del self.data[note_id]
