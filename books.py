"""Repositories for contacts and standalone notes, both keyed by stable ids."""
 
from collections import UserDict
 
from upcoming_birthdays import get_upcoming_birthdays
 
 
MAX_UPCOMING_DAYS = 365
 
 
def _text(value) -> str:
    """Return a plain string for a field object, a raw value or ``None``."""
    if value is None:
        return ""
    inner = getattr(value, "value", value)
    if inner is None:
        return ""
    return str(inner)
 
 
def _normalize(value) -> str:
    """Case-insensitive, whitespace-collapsed form used for lookups."""
    return " ".join(_text(value).split()).casefold()
 
 
def _iter_values(value):
    """Yield every element of a collection field, or the field itself."""
    if value is None:
        return
    if isinstance(value, (str, bytes)) or not hasattr(value, "__iter__"):
        yield value
        return
    yield from value
 
 
def _digits(value: str) -> str:
    return "".join(char for char in value if char.isdigit())
 
 
class AddressBook(UserDict):
    """Store ``Contact`` objects as ``{contact_id: contact}``."""
 
    def add(self, contact):
        """Reject a duplicate normalized contact name, then store contact."""
        name = _normalize(getattr(contact, "name", None))
        if not name:
            raise ValueError("Contact name cannot be empty.")
 
        for existing in self.data.values():
            if _normalize(getattr(existing, "name", None)) == name:
                raise ValueError(
                    f"Contact '{_text(getattr(contact, 'name', None))}' already exists."
                )
 
        contact_id = _text(getattr(contact, "id", None))
        if not contact_id:
            raise ValueError("Contact must have an id.")
        if contact_id in self.data:
            raise ValueError(f"Contact with id '{contact_id}' already exists.")
 
        self.data[contact_id] = contact
        return contact
 
    def find_by_id(self, contact_id: str):
        """Return a Contact by id, or None."""
        return self.data.get(_text(contact_id))
 
    def search(self, query: str):
        """Return every partial, case-insensitive match across name,
        phone, email, address and birthday."""
        needle = _normalize(query)
        if not needle:
            raise ValueError("Search query cannot be empty.")
 
        digits = _digits(needle)
        matches = []
 
        for contact in self.data.values():
            haystack = self._searchable_parts(contact)
            if any(needle in part for part in haystack):
                matches.append(contact)
                continue
            if digits and any(digits in _digits(part) for part in haystack):
                matches.append(contact)
 
        return matches
 
    @staticmethod
    def _searchable_parts(contact):
        """Flatten every searchable field of a contact into normalized strings."""
        fields = ("name", "phones", "phone", "emails", "email", "address", "birthday")
        parts = []
        for field in fields:
            for value in _iter_values(getattr(contact, field, None)):
                normalized = _normalize(value)
                if normalized:
                    parts.append(normalized)
        return parts
 
    def delete(self, contact_id: str):
        """Delete a Contact by id or report it missing. Confirmation is
        performed by the user-facing command before this method is called."""
        key = _text(contact_id)
        if key not in self.data:
            raise KeyError(f"Contact with id '{key}' was not found.")
        return self.data.pop(key)
 
    def get_upcoming_birthdays(self, days: int):
        """Validate days and delegate the calculation to the helper."""
        if isinstance(days, bool) or not isinstance(days, int):
            try:
                days = int(str(days).strip())
            except (TypeError, ValueError) as error:
                raise ValueError("Number of days must be an integer.") from error
 
        if days < 1 or days > MAX_UPCOMING_DAYS:
            raise ValueError(
                f"Number of days must be between 1 and {MAX_UPCOMING_DAYS}."
            )
 
        return get_upcoming_birthdays(list(self.data.values()), days)
 
 
class NotesBook(UserDict):
    """Store standalone ``Note`` objects as ``{note_id: note}``."""
 
    def add(self, note):
        """Reject a duplicate id and store note."""
        note_id = _text(getattr(note, "id", None))
        if not note_id:
            raise ValueError("Note must have an id.")
        if note_id in self.data:
            raise ValueError(f"Note with id '{note_id}' already exists.")
 
        self.data[note_id] = note
        return note
 
    def find_by_id(self, note_id: str):
        """Return a Note by id, or None."""
        return self.data.get(_text(note_id))
 
    def search(self, query: str):
        """Return every note whose text partially matches query."""
        needle = _normalize(query)
        if not needle:
            raise ValueError("Search query cannot be empty.")
 
        return [
            note
            for note in self.data.values()
            if needle in _normalize(getattr(note, "text", None))
        ]
 
    def search_by_tag(self, tag: str):
        """Normalize tag and return every note that contains it."""
        needle = _normalize(tag).lstrip("#")
        if not needle:
            raise ValueError("Tag cannot be empty.")
 
        return [
            note
            for note in self.data.values()
            if needle in self._tags(note)
        ]
 
    def sort_by_tags(self):
        """Return all notes ordered by tags, with untagged notes last;
        use text or id as a deterministic tie-breaker."""
 
        def sort_key(note):
            tags = sorted(self._tags(note))
            return (
                not tags,
                tags,
                _normalize(getattr(note, "text", None)),
                _text(getattr(note, "id", None)),
            )
 
        return sorted(self.data.values(), key=sort_key)
 
    @staticmethod
    def _tags(note):
        """Return the normalized, de-duplicated tags of a note."""
        tags = set()
        for value in _iter_values(getattr(note, "tags", None)):
            normalized = _normalize(value).lstrip("#")
            if normalized:
                tags.add(normalized)
        return tags
 
    def delete(self, note_id: str):
        """Delete a Note by id or report it missing. Confirmation is
        performed by the user-facing command before this method is called."""
        key = _text(note_id)
        if key not in self.data:
            raise KeyError(f"Note with id '{key}' was not found.")
        return self.data.pop(key)