from datetime import date, timedelta


def get_upcoming_birthdays(address_book, days: int):
    today = date.today()
    upcoming_birthdays = []

    for contact in address_book.data.values():
        if contact.birthday is None:
            continue

        birthday = contact.birthday.value

        try:
            birthday_this_year = birthday.replace(year=today.year)
        except ValueError:
            birthday_this_year = date(today.year, 2, 28)

        if birthday_this_year < today:
            try:
                birthday_this_year = birthday.replace(year=today.year + 1)
            except ValueError:
                birthday_this_year = date(today.year + 1, 2, 28)

        if 0 <= (birthday_this_year - today).days <= days:
            congratulation_date = birthday_this_year

            if congratulation_date.weekday() == 5:
                congratulation_date += timedelta(days=2)
            elif congratulation_date.weekday() == 6:
                congratulation_date += timedelta(days=1)

            upcoming_birthdays.append(
                {
                    "id": contact.id,
                    "name": contact.name.value,
                    "congratulation_date": congratulation_date.strftime("%d.%m.%Y"),
                }
            )

    return upcoming_birthdays
