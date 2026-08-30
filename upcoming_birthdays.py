"""
Upcoming Birthdays Handler Module.
Provides functionality to calculate and retrieve a list of contacts with
birthdays occurring within a specified number of days, adjusting weekend dates
to the following Monday.
"""
from datetime import date, timedelta
from typing import Iterable

from models import Contact


def get_upcoming_birthdays(
    contacts: Iterable[Contact], days: int
) -> list[dict[str, str]]:
    today = date.today()
    upcoming_birthdays = []

    for contact in contacts:
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
