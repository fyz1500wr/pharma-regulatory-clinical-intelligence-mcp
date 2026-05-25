from datetime import date
from src.core.date_utils import resolve_date_range


def test_date_ranges():
    end = date(2026, 5, 25)
    s, e = resolve_date_range("1m", end_date=end)
    assert e == end and (end - s).days >= 28
    cstart = date(2026, 1, 1)
    s2, _ = resolve_date_range("custom", end_date=end, start_date=cstart)
    assert s2 == cstart
