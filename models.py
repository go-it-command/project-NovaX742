import re
from datetime import datetime

"""Validated domain models for contacts and standalone notes."""


class Field:
    """Base value object for validated contact fields."""

    def __init__(self, value):
        # TODO: Store a normalized, already validated value.
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    """Required contact name; trim whitespace and reject an empty value."""
    # TODO: Validate while retaining Unicode names (including Ukrainian names).

    def __init__(self, value: str):
        normalized_value = value.strip()

        if not normalized_value:
            raise ValueError("Ім’я контакту не може бути порожнім.")

        super().__init__(normalized_value)


class Phone(Field):
    """Normalized and validated phone number."""
    # TODO: Remove spaces, brackets and hyphens; validate the agreed phone
    # format (10 digits or an international number such as +380...).

    def __init__(self, value: str):
        normalized_value = (
            value.strip()
            .replace(" ", "")
            .replace("-", "")
            .replace("(", "")
            .replace(")", "")
        )

        local_phone_is_valid = (
            len(normalized_value) == 10
            and normalized_value.isdigit()
        )

        international_phone_is_valid = (
            normalized_value.startswith("+")
            and normalized_value[1:].isdigit()
            and 10 <= len(normalized_value[1:]) <= 15
        )

        if not local_phone_is_valid and not international_phone_is_valid:
            raise ValueError(
                "Некоректний номер телефону. Введіть 10 цифр "
                "або міжнародний номер у форматі + та від 10 до 15 цифр."
            )

        super().__init__(normalized_value)


class Email(Field):
    """Normalized, lower-case email address."""
    # TODO: Trim/lowercase and validate a basic name@domain.tld structure.

    def __init__(self, value: str):
        normalized_value = value.strip().lower()

        email_pattern = r"^[^\s@]+@[^\s@]+\.[^\s@]+$"

        if not re.fullmatch(email_pattern, normalized_value):
            raise ValueError(
                "Некоректна електронна адреса. "
                "Використовуйте формат name@domain.tld."
            )

        super().__init__(normalized_value)


class Address(Field):
    """Required non-empty address value."""
    # TODO: Trim whitespace and reject an empty value.

    def __init__(self, value: str):
        normalized_value = value.strip()

        if not normalized_value:
            raise ValueError("Адреса не може бути порожньою.")
        
        super().__init__(normalized_value)


class Birthday(Field):
    """Birthday parsed from DD.MM.YYYY and stored as a date."""
    # TODO: Parse the date and report invalid calendar dates clearly.

    def __init__(self, value: str):
        try:
            birthday_date = datetime.strptime(value.strip(),"%d.%m.%Y",).date()
        except(ValueError, AttributeError) as error:
            raise ValueError(
               "Некоректна дата народження. "
               "Використовуйте формат DD.MM.YYYY." 
            ) from error

        super().__init__(birthday_date)


class Contact:
    """One contact, identified by a stable id and independent from notes."""

    def __init__(self, contact_id: str, name: str):
        # TODO: Generate contact_id with uuid4() before calling this constructor.
        self.id = contact_id
        self.name = Name(name)
        self.phone = None
        self.email = None
        self.address = None
        self.birthday = None

    def set_phone(self, phone: str):
        # TODO: Validate and set/replace the optional Phone field.
        
        self.phone = Phone(phone)

    def set_name(self, name: str):
        # TODO: Validate and replace the Name field.

        self.name = Name(name)

    def set_email(self, email: str):
        # TODO: Validate and replace the optional Email field.
        
        self.email = Email(email)

    def set_address(self, address: str):
        # TODO: Validate and replace the optional Address field.
        
        self.address = Address(address)

    def set_birthday(self, birthday: str):
        # TODO: Validate and replace the optional Birthday field.
        
        self.birthday = Birthday(birthday)

    def __str__(self):
        # TODO: Display id, name, phone, email, address and birthday; render
        # absent optional values as an em dash rather than None.
        
        phone = self.phone.value if self.phone else "—"
        email = self.email.value if self.email else "—"
        address = self.address.value if self.address else "—"

        birthday = (
            self.birthday.value.strftime("%d.%m.%Y")
            if self.birthday
            else "-"
        )

        return (
            f"ID: {self.id}, "
            f"Name: {self.name.value}, "
            f"Phone: {phone}, "
            f"Email: {email}, "
            f"Address: {address}, "
            f"Birthday: {birthday}"
        )


class Note:
    """Standalone note identified by a stable id with optional unique tags."""

    def __init__(self, note_id: str, text: str, tags=None):
        # TODO: Generate note_id with uuid4(), validate text and normalize tags
        # before creating this object.
        self.id = note_id
        self.text = text
        self.tags = set(tags or [])

    def edit_text(self, text: str):
        # TODO: Trim text and reject an empty value before replacing it.
        pass

    def add_tag(self, tag: str):
        # TODO: Remove #/whitespace, lowercase the tag and add it if unique.
        pass

    def edit_tag(self, old_tag: str, new_tag: str):
        # TODO: Ensure old_tag exists and replace it with normalized new_tag.
        pass

    def delete_tag(self, tag: str):
        # TODO: Remove a normalized tag or report that it does not exist.
        pass

    def __str__(self):
        # TODO: Display id, text and tags sorted alphabetically.
        pass
