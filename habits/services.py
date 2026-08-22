from datetime import timedelta

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
        while current < pause.end_date:
            days.add(current)
            current += timedelta(days=1)
    return days