from django.test import TestCase
from datetime import date
from habits.services import paused_days

class FakePause:
    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date

def test_single_day_pause_counts():
    day = date(2026, 8, 25)
    assert paused_days([FakePause(day, day)]) == {day}

def test_pause_includes_both_ends():
    result = paused_days([FakePause(date(2026, 8, 5), date(2026, 8, 7))])
    assert result == {date(2026, 8, 5), date(2026, 8, 6), date(2026, 8, 7)}