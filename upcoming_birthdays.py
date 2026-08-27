"""Calculate which contacts should be congratulated within the next N days."""
 
from datetime import date, datetime, timedelta
 
DATE_FORMAT = "%d.%m.%Y"
INPUT_FORMATS = ("%d.%m.%Y", "%Y-%m-%d", "%d/%m/%Y")
 
# A 29 February birthday is observed on 1 March in non-leap years.
# Set to False to observe it on 28 February instead.
LEAP_DAY_AFTER_FEBRUARY = True
 
 
def _as_date(value):
    """Return a ``date`` for a Birthday field, a date/datetime or a string."""
    raw = getattr(value, "value", value)
    if raw is None:
        return None
    if isinstance(raw, datetime):
        return raw.date()
    if isinstance(raw, date):
        return raw
 
    text = str(raw).strip()
    for fmt in INPUT_FORMATS:
        try:
            return datetime.strptime(text, fmt).date()
        except ValueError:
            continue
    return None
 
 
def _birthday_this_year(birthday: date, year: int) -> date:
    """Return the birthday in ``year``, handling 29 February in non-leap years."""
    try:
        return birthday.replace(year=year)
    except ValueError:
        # 29 February in a non-leap year.
        return date(year, 3, 1) if LEAP_DAY_AFTER_FEBRUARY else date(year, 2, 28)
 
 
def _shift_from_weekend(day: date) -> date:
    """Move a Saturday or Sunday date to the following Monday."""
    weekday = day.weekday()
    if weekday >= 5:  # 5 = Saturday, 6 = Sunday
        return day + timedelta(days=7 - weekday)
    return day
 
 
def get_upcoming_birthdays(book, days: int, today: date | None = None) -> list:
    """Return ``[{'id', 'name', 'congratulation_date'}, ...]`` for contacts whose
    birthday falls within ``days`` days from today, inclusive of the boundary.
    """
    today = today or date.today()
    horizon = today + timedelta(days=days)
    upcoming = []
 
    for contact in book.data.values():
        birthday = _as_date(getattr(contact, "birthday", None))
        if birthday is None:
            continue
 
        celebration = _birthday_this_year(birthday, today.year)
        if celebration < today:
            celebration = _birthday_this_year(birthday, today.year + 1)
 
        if celebration > horizon:
            continue
 
        upcoming.append(
            {
                "id": str(getattr(contact, "id", "")),
                "name": str(getattr(contact, "name", "")),
                "congratulation_date": _shift_from_weekend(celebration).strftime(
                    DATE_FORMAT
                ),
            }
        )
 
    upcoming.sort(key=lambda item: datetime.strptime(
        item["congratulation_date"], DATE_FORMAT
    ))
    return upcoming