"""Interactive CLI commands for contact management."""

import uuid

from models import Contact


def _select_contact(args, contacts):
    """Return one contact selected by UUID or a search query."""
    if not args:
        return None

    if len(args) == 1:
        try:
            uuid.UUID(args[0])
            return contacts.find_by_id(args[0])
        except ValueError:
            pass

    matches = contacts.search(" ".join(args))
    if not matches:
        return None
    if len(matches) == 1:
        return matches[0]

    contact_list = "\n".join(
        f"{contact.id} — {contact.name.value}" for contact in matches
    )
    selected_id = input(
        f"Found several contacts:\n{contact_list}\nEnter contact UUID: "
    ).strip()
    return next(
        (contact for contact in matches if contact.id == selected_id),
        None,
    )


def _ask_optional_field(prompt, setter):
    """Set an optional field or return when the user skips it."""
    while True:
        value = input(prompt).strip()
        if not value:
            return
        try:
            setter(value)
            return
        except ValueError as error:
            print(f"Error: {error}")


def add_contact(contacts):
    """Create a contact through an interactive dialogue."""
    while True:
        try:
            contact = Contact(str(uuid.uuid4()), input("Name: ").strip())
            break
        except ValueError as error:
            print(f"Error: {error}")

    _ask_optional_field("Phone (press Enter to skip): ", contact.set_phone)
    _ask_optional_field("Email (press Enter to skip): ", contact.set_email)
    _ask_optional_field("Address (press Enter to skip): ", contact.set_address)
    _ask_optional_field(
        "Birthday (DD.MM.YYYY, press Enter to skip): ",
        contact.set_birthday,
    )
    contacts.add(contact)
    return f"Contact added: {contact}"


def change_contact(args, contacts):
    """Change one field of a selected contact."""
    contact = _select_contact(args, contacts)
    if contact is None:
        return "Contact not found."

    setters = {
        "name": contact.set_name,
        "phone": contact.set_phone,
        "email": contact.set_email,
        "address": contact.set_address,
        "birthday": contact.set_birthday,
    }
    field = input("Field (name/phone/email/address/birthday): ").strip().lower()
    setter = setters.get(field)
    if setter is None:
        return "Invalid field. Choose name, phone, email, address or birthday."

    value = input(f"New {field}: ").strip()
    if not value:
        return "Value cannot be empty."
    try:
        setter(value)
    except ValueError as error:
        return f"Error: {error}"
    return f"Contact updated: {contact}"


def find_contact(args, contacts):
    """Find contacts by a partial query across searchable fields."""
    if not args:
        return "Usage: find-contact <query>"

    matches = contacts.search(" ".join(args))
    if not matches:
        return "No contacts found."
    return "\n".join(str(contact) for contact in matches)


def delete_contact(args, contacts):
    """Delete a selected contact after explicit confirmation."""
    contact = _select_contact(args, contacts)
    if contact is None:
        return "Contact not found."

    print(f"Found contact: {contact}")
    confirmation = input("Are you sure? (yes/no): ").strip().lower()
    if confirmation != "yes":
        return "Deletion cancelled."

    contacts.delete(contact.id)
    return "Contact deleted."


def birthdays(args, contacts):
    """Show contacts with birthdays in the requested number of days."""
    if len(args) != 1:
        return "Usage: birthdays <days>"

    try:
        days = int(args[0])
        upcoming = contacts.get_upcoming_birthdays(days)
    except ValueError as error:
        return f"Error: {error}"

    if not upcoming:
        return "No upcoming birthdays."
    return "\n".join(
        f"{item['name']}: {item['congratulation_date']}" for item in upcoming
    )
