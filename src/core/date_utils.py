from datetime import date, timedelta


def _subtract_months(d: date, months: int) -> date:
    return d - timedelta(days=months * 30)


def _subtract_years(d: date, years: int) -> date:
    return d - timedelta(days=years * 365)


def resolve_date_range(date_range: str, *, end_date: date | None = None, start_date: date | None = None) -> tuple[date, date]:
    end = end_date or date.today()
    if date_range == "custom":
        if not start_date:
            raise ValueError("custom range requires start_date")
        return start_date, end
    mapping = {
        "1m": lambda d: _subtract_months(d, 1),
        "3m": lambda d: _subtract_months(d, 3),
        "6m": lambda d: _subtract_months(d, 6),
        "1y": lambda d: _subtract_years(d, 1),
        "3y": lambda d: _subtract_years(d, 3),
        "5y": lambda d: _subtract_years(d, 5),
    }
    if date_range not in mapping:
        raise ValueError(f"unsupported date_range: {date_range}")
    return mapping[date_range](end), end
