from .models import Completion, Habit, Pause
from .services import paused_days

def completion_by_habit(user):
    result = {}
    rows = Completion.objects.filter(habit__user=user).values_list("habit_id", "date")
    for habit_id, day in rows:
        result.setdefault(habit_id, set()).add(day)
    return result

def paused_dates_for(user):
    return paused_days(Pause.objects.filter(user=user))