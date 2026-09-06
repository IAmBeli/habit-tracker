from datetime import date
from habits.services import is_due, paused_days, current_streak
from habits.services import month_summary

class FakeHabit:
    def __init__(self, id, start_date, interval_days):
        self.id = id
        self.start_date = start_date
        self.interval_days = interval_days

class FakePause:
    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date

def test_due_on_start():
    start = date(2026, 8, 1)
    assert is_due(start, 3, start)

def test_due_every_third_day():
    start = date(2026, 8, 1)
    due = [d for d in range(1, 11) if is_due(start, 3, date(2026, 8, d))]
    assert due == [1, 4, 7, 10]

def test_not_due_before_start():
    start = date(2026, 8, 10)
    assert not is_due(start, 3, date(2026, 8, 7))

def test_daily_habit_is_due_every_day():
    start = date(2026, 8, 1)
    assert all(is_due(start, 1, date(2026, 8, d)) for d in range(1, 8))

def test_single_day_pause_counts():
    day = date(2026, 8, 25)
    assert paused_days([FakePause(day, day)]) == {day}

def test_pause_include_both_ends():
    result = paused_days([FakePause(date(2026, 8, 5), date(2026, 8, 7))])
    assert result == {date(2026, 8, 5), date(2026, 8, 6), date(2026, 8, 7)}

def test_no_pause_gives_empty_set():
    assert paused_days([]) == set()

START = date(2026, 8, 1)

def test_no_completions_gives_zero():
    assert current_streak(START, 3, date(2026, 8, 10), set(), set()) == 0

def test_counts_consecutive_due_days():
    done = {date(2026, 8, 4), date(2026, 8, 7), date(2026, 8, 10)}
    assert current_streak(START, 3, date(2026, 8, 10), done, set()) == 3

def test_breaks_on_missed_day():
    done = {date(2026, 8, 1), date(2026, 8, 7), date(2026, 8, 10)}
    assert current_streak(START, 3, date(2026, 8, 10), done, set()) == 2

def test_ignores_non_due_completions():
    done = {date(2026, 8, 10), date(2026, 8, 9), date(2026, 8, 8)}
    assert current_streak(START, 3, date(2026, 8, 10), done, set()) == 1

def test_pause_does_not_break_streak():
    done = {date(2026, 8, 1), date(2026, 8, 10)}
    paused = {date(2026, 8, 4), date(2026, 8, 7)}
    assert current_streak(START, 3, date(2026, 8, 10), done, paused) == 2

def test_pause_does_not_increase_streak():
    done = {date(2026, 8, 10)}
    paused = {date(2026, 8, 7)}
    assert current_streak(START, 3, date(2026, 8, 10), done, paused) == 1

def test_blank_cells_before_first_day():
    days = month_summary(2026, 8, [], {}, set())
    blanks = [d for d in days if d["state"] == "blank"]
    assert len(blanks) == 5

def test_month_has_all_days():
    days = month_summary(2026, 8, [], {}, set())
    real = [d for d in days if d["date"] is not None]
    assert len(real) == 31

def test_day_is_full_when_all_done():
    habit = FakeHabit(1, date(2026, 8, 1), 1)
    done = {1: {date(2026, 8, 3)}}
    days = month_summary(2026, 8, [habit], done, set())
    third = next(d for d in days if d["date"] == date(2026, 8, 3))
    assert third["state"] == "full"

def test_paused_day_shows_as_paused():
    habit = FakeHabit(1, date(2026, 8, 1), 1)
    days = month_summary(2026, 8, [habit], {}, {date(2026, 8, 3)})
    third = next(d for d in days if d["date"] == date(2026, 8, 3))
    assert third["state"] == "paused"

def test_pause_visible_without_due_habits():
    days = month_summary(2026, 8, [], {}, {date(2026, 8, 3)})
    third = next(d for d in days if d["date"] == date(2026, 8, 3))
    assert third["state"] == "paused"