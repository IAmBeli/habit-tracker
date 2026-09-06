from datetime import timedelta, date
from calendar import monthrange

def is_due(start_date, interval_days, on_date):
    if on_date < start_date:
        return False
    return (on_date - start_date).days % interval_days == 0

def due_dates_until(start_date, interval_days, until_date):
    dates = []
    current = start_date
    while current <= until_date:
        dates.append(current)
        current += timedelta(days=interval_days)
    return dates

def current_streak(start_date, interval_days, until_date, done_dates, paused_dates):
    streak = 0
    for due in reversed(due_dates_until(start_date, interval_days, until_date)):
        if due in paused_dates:
            continue
        if due in done_dates:
            streak += 1
        else:
            break
    return streak

def paused_days(pauses):
    days = set()
    for pause in pauses:
        current = pause.start_date
        while current <= pause.end_date:
            days.add(current)
            current += timedelta(days=1)
    return days

def month_dates(year, month):
    days_in_month = monthrange(year, month)[1]
    return [date(year, month, day) for day in range(1, days_in_month + 1)]

def month_summary(year, month, habits, done_by_habit, paused_dates):
    first_weekday = monthrange(year, month)[0]
    result = [{"date": None, "state": "blank"} for _ in range(first_weekday)]
    
    for day in month_dates(year, month):
        due = [
            habit for habit in habits
            if is_due(habit.start_date, habit.interval_days, day)
        ]

        if day in paused_dates:
            state = "paused"
        elif not due:
            state = "empty"
        else:
            done_count = sum(
                1 for habit in due
                if day in done_by_habit.get(habit.id, set())
            )
            if done_count == len(due):
                state = "full"
            elif done_count > 0:
                state = "partial"
            else:
                state = "none"
        result.append({"date": day, "state": state})
    return result