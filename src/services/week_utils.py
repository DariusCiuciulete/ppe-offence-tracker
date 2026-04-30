from datetime import date, timedelta


def _first_sunday(year: int) -> date:
    january_first = date(year, 1, 1)
    days_until_sunday = (6 - january_first.weekday()) % 7
    return january_first + timedelta(days=days_until_sunday)


def get_operational_week(target_date: date) -> dict:
    week_year = target_date.year
    year_start = date(week_year, 1, 1)
    first_sunday = _first_sunday(week_year)

    if target_date < first_sunday:
        week_number = 1
        week_start = year_start
        week_end = first_sunday - timedelta(days=1)
    else:
        days_since_sunday = (target_date.weekday() + 1) % 7
        week_start = target_date - timedelta(days=days_since_sunday)
        week_end = week_start + timedelta(days=6)

        if first_sunday == year_start:
            week_number = ((week_start - first_sunday).days // 7) + 1
        else:
            week_number = ((week_start - first_sunday).days // 7) + 2

    return {
        "week_year": week_year,
        "week_number": week_number,
        "week_start": week_start,
        "week_end": week_end,
        "label": f"Week {week_number} ({week_start.isoformat()} to {week_end.isoformat()})",
    }
