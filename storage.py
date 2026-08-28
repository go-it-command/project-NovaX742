import pickle
from pathlib import Path

from books import AddressBook, NotesBook


DATA_FILE = Path.home() / "assistant_data.pkl"


def save_data(contacts: AddressBook, notes: NotesBook) -> None:
    with DATA_FILE.open("wb") as file:
        pickle.dump((contacts, notes), file)


def load_data() -> tuple[AddressBook, NotesBook]:
    try:
        with DATA_FILE.open("rb") as file:
            return pickle.load(file)
    except (FileNotFoundError, EOFError, pickle.UnpicklingError, AttributeError):
        return AddressBook(), NotesBook()
