import pytest
from datetime import date
from habits.forms import PauseForm

def test_pause_rejects_reversed_dates():
    form = PauseForm(data={
        "start_date": date(2026, 8, 10),
        "end_date": date(2026, 8, 5),
        "reason": "sick",
    })
    assert not form.is_valid()

def test_pause_accepts_same_day():
    day = date(2026, 8, 10)
    form = PauseForm(data={"start_date": day, "end_date": day, "reason": "sick"})
    assert form.is_valid()