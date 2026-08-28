# CLI-сценарії для роботи з контактами
# (Задача 3 — команди контактів і збірка CLI)

import uuid
from models import Contact


"""
1. `input('Name: ')`; якщо порожньо — перепитати.
2. По черзі запитати `Phone`, `Email`, `Address`, `Birthday`.
3. Для необов’язкових полів порожній Enter означає «пропустити».
4. Якщо setter дав `ValueError`, показати текст помилки й перепитати саме це
   поле.
5. Згенерувати `str(uuid.uuid4())`, створити `Contact(id, name)`.
6. Викликати setters для полів, які не пропущені.
7. Викликати `contacts.add(contact)`.
8. Повернути `Contact added: <contact>`.
"""
# приватна ф-ція модуля
# Повертає один конкретний контакт або None.
def _select_contact(args, contacts):
    if not args:
        return None

    # Якщо передано один UUID, шукаємо безпосередньо за id.
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

    # Не вибираємо перший збіг автоматично: користувач має вказати UUID.
    contact_list = "\n".join(
        f"{contact.id} — {contact.name.value}" for contact in matches
    )
    selected_id = input(
        f"Found several contacts:\n{contact_list}\nEnter contact UUID: "
    ).strip()

    for contact in matches:
        if contact.id == selected_id:
            return contact

    return None


# приватна ф-ція модуля
# Запитує необов'язкове поле та повторює ввід після ValueError.
def _ask_optional_field(request, setter):
    while True:
        value = input(request).strip()
        if not value:
            return False

        try:
            setter(value)
            return True
        except ValueError as error:
            # Помилку показуємо через наступний request, не використовуючи print().
            request = f"{error}\n{request}"


"""
1. `input('Name: ')`; якщо порожньо — перепитати.
2. По черзі запитати `Phone`, `Email`, `Address`, `Birthday`.
3. Для необов’язкових полів порожній Enter означає «пропустити».
4. Якщо setter дав `ValueError`, показати текст помилки й перепитати саме це
   поле.
5. Згенерувати `str(uuid.uuid4())`, створити `Contact(id, name)`.
6. Викликати setters для полів, які не пропущені.
7. Викликати `contacts.add(contact)`.
8. Повернути `Contact added: <contact>`.
"""
# Інтерактивно створює новий контакт.
def add_contact(contacts):
    while True:
        name = input("Name: ").strip()
        if name:
            break
        # Повторюємо запит, оскільки ім'я є обов'язковим.
        name = input("Name cannot be empty. Please enter a name.\nName: ").strip()

    contact_id = str(uuid.uuid4())
    contact = Contact(contact_id, name)

    _ask_optional_field("Phone: ", contact.set_phone)
    _ask_optional_field("Email: ", contact.set_email)
    _ask_optional_field("Address: ", contact.set_address)
    _ask_optional_field("Birthday: ", contact.set_birthday)

    try:
        contacts.add(contact)
    except ValueError as error:
        return str(error)

    return f"Contact added: {contact}"


"""
1. Через допоміжну функцію вибрати контакт.
2. Запитати `Field (name/phone/email/address/birthday):`.
3. Якщо поле не з цього списку — повідомити помилку.
4. Запитати нове значення.
5. Викликати відповідний `contact.set_*`.
6. Повернути оновлений контакт.
"""
# Знаходить контакт і змінює одне з його полів.
def change_contact(args, contacts):
    contact = _select_contact(args, contacts)
    if contact is None:
        return "Contact not found."

    fields = {
        "name": contact.set_name,
        "phone": contact.set_phone,
        "email": contact.set_email,
        "address": contact.set_address,
        "birthday": contact.set_birthday,
    }

    field = input("Field (name/phone/email/address/birthday): ").strip().lower()
    if field not in fields:
        return "Invalid field. Choose name, phone, email, address or birthday."

    value = input(f"New {field}: ").strip()
    if not value:
        return "Value cannot be empty."

    try:
        fields[field](value)
    except ValueError as error:
        return str(error)

    return f"Contact updated: {contact}"


"""
- якщо немає args — пояснити формат;
- інакше `contacts.search(' '.join(args))`;
- повернути всі знайдені контакти або `No contacts found.`.
"""
# Шукає контакти за довільним текстовим запитом.
def find_contact(args, contacts):
    if not args:
        return "Usage: find-contact <query>"

    matches = contacts.search(" ".join(args))
    if not matches:
        return "No contacts found."

    return "\n".join(str(contact) for contact in matches)


"""
1. Вибрати один контакт.
2. Повернути/показати його дані.
3. `input('Are you sure? (yes/no): ')`.
4. Тільки `yes` → `contacts.delete(contact.id)` і `Contact deleted.`.
5. Будь-яка інша відповідь → `Deletion cancelled.`.
"""
# Знаходить контакт, просить підтвердження та видаляє його.
def delete_contact(args, contacts):
    contact = _select_contact(args, contacts)
    if contact is None:
        return "Contact not found."

    confirmation = input(
        f"{contact}\nAre you sure? (yes/no): "
    ).strip().lower()

    if confirmation == "yes":
        contacts.delete(contact.id)
        return "Contact deleted."

    return "Deletion cancelled."


"""
- один аргумент;
- перетворити у `int`, від’ємне заборонити;
- викликати `contacts.get_upcoming_birthdays(days)`;
- відформатувати name і congratulation_date або `No upcoming birthdays.`.
"""
# Показує найближчі дні народження на задану кількість днів.
def birthdays(args, contacts):
    if len(args) != 1:
        return "Usage: birthdays <days>"

    try:
        days = int(args[0])
    except ValueError:
        return "Days must be an integer."

    if days < 0:
        return "Days cannot be negative."

    upcoming = contacts.get_upcoming_birthdays(days)
    if not upcoming:
        return "No upcoming birthdays."

    return "\n".join(
        f"{item['name']}: {item['congratulation_date']}"
        for item in upcoming
    )
