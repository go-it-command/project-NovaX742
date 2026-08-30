"""Validated domain models for contacts and standalone notes."""

import re
from datetime import datetime
from typing import Iterable

from utils import normalize_tag


class Field:
    """Base value object for validated contact fields."""

    def __init__(self, value: object) -> None:
        self.value = value

    def __str__(self) -> str:
        return str(self.value)


class Name(Field):
    """Required contact name; trim whitespace and reject an empty value."""

    def __init__(self, value: str) -> None:
        normalized_value = value.strip()

        if not normalized_value:
            raise ValueError(
                "Ім’я контакту не може бути порожнім."
            )

        super().__init__(normalized_value)


class Phone(Field):
    """Normalized and validated phone number."""

    def __init__(self, value: str) -> None:
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
                "Некоректний номер телефону. "
                "Введіть 10 цифр або "
                "міжнародний номер у форматі "
                "+ та від 10 до 15 цифр."
            )

        super().__init__(normalized_value)


class Email(Field):
    """Normalized, lower-case email address."""

    def __init__(self, value: str) -> None:
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

    def __init__(self, value: str) -> None:
        normalized_value = value.strip()

        if not normalized_value:
            raise ValueError("Адреса не може бути порожньою.")

        super().__init__(normalized_value)


class Birthday(Field):
    """Birthday parsed from DD.MM.YYYY and stored as a date."""

    def __init__(self, value: str) -> None:
        try:
            birthday_date = datetime.strptime(value.strip(), "%d.%m.%Y").date()
        except (ValueError, AttributeError) as error:
            raise ValueError(
                "Некоректна дата народження. "
                "Використовуйте формат DD.MM.YYYY."
            ) from error

        super().__init__(birthday_date)


class Contact:
    """One contact, identified by a stable id and independent from notes."""

    def __init__(self, contact_id: str, name: str) -> None:
        self.id = contact_id
        self.name = Name(name)
        self.phone: Phone | None = None
        self.email: Email | None = None
        self.address: Address | None = None
        self.birthday: Birthday | None = None

    def set_phone(self, phone: str) -> None:
        self.phone = Phone(phone)

    def set_name(self, name: str) -> None:
        self.name = Name(name)

    def set_email(self, email: str) -> None:
        self.email = Email(email)

    def set_address(self, address: str) -> None:
        self.address = Address(address)

    def set_birthday(self, birthday: str) -> None:
        self.birthday = Birthday(birthday)

    def __str__(self) -> str:
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

    def __init__(
        self,
        note_id: str,
        text: str,
        tags: Iterable[str] | None = None,
    ) -> None:
        self.id = note_id
        self.text: str = ""
        self.tags: set[str] = set()

        self.edit_text(text)

        if tags:
            for tag in tags:
                self.add_tag(tag)

    def edit_text(self, text: str) -> None:
        normalized_text = text.strip()

        if not normalized_text:
            raise ValueError(
                "Текст нотатки не може бути порожнім."
            )

        self.text = normalized_text

    def add_tag(self, tag: str) -> None:
        normalized_tag = normalize_tag(tag)
        self.tags.add(normalized_tag)

    def edit_tag(self, old_tag: str, new_tag: str) -> None:
        normalized_old_tag = normalize_tag(old_tag)
        normalized_new_tag = normalize_tag(new_tag)

        if normalized_old_tag not in self.tags:
            raise ValueError(f'Тег "{normalized_old_tag}" не знайдено.')

        self.tags.remove(normalized_old_tag)
        self.tags.add(normalized_new_tag)

    def delete_tag(self, tag: str) -> None:
        normalized_tag = normalize_tag(tag)

        if normalized_tag not in self.tags:
            raise ValueError(f'Тег "{normalized_tag}" не знайдено.')

        self.tags.remove(normalized_tag)

    def __str__(self) -> str:
        tags = ", ".join(sorted(self.tags)) if self.tags else "—"

        return (
            f"ID: {self.id}, "
            f"Text: {self.text}, "
            f"Tags: {tags}"
        )
