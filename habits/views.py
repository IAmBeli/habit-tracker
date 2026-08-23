from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Completion, Habit, Pause
from .services import is_due, current_streak, paused_days
from .forms import HabitForm, PauseForm

@login_required
def today(request):
    current_date = timezone.localdate()

    habits = Habit.objects.filter(user=request.user, is_active=True)

    completions = Completion.objects.filter(habit__user=request.user)
    done_by_habit={}
    for habit_id, date in completions.values_list("habit_id", "date"):
        done_by_habit.setdefault(habit_id, set()).add(date)

    pauses = paused_days(Pause.objects.filter(user=request.user))

    items=[]
    for habit in habits:
        if not is_due(habit.start_date, habit.interval_days, current_date):
            continue
        done_dates = done_by_habit.get(habit.id, set())
        items.append({
            "habit": habit,
            "is_done": current_date in done_dates,
            "streak": current_streak(
                habit.start_date,
                habit.interval_days,
                current_date,
                done_dates,
                pauses,
            ),
        })
    return render(request, "habits/today.html", {"items": items, "date": current_date,})

@login_required
def toggle(request, habit_id):
    if request.method != "POST":
        return redirect("today")

    habit = get_object_or_404(Habit, pk=habit_id, user=request.user)
    current_date = timezone.localdate()

    completion, created = Completion.objects.get_or_create(
        habit=habit,
        date=current_date,
    )
    if not created:
        completion.delete()

    return redirect("today")

@login_required
def create_habit(request):
    if request.method == "POST":
        form = HabitForm(request.POST)
        if form.is_valid():
            habit = form.save(commit=False)
            habit.user = request.user
            habit.save()
            return redirect("today")
    else:
        form = HabitForm()

    return render(request, "habits/habit_form.html", {"form": form})

@login_required
def habit_list(request):
    habits = Habit.objects.filter(user=request.user).order_by("title")
    return render(request, "habits/habit_list.html", {"habits": habits})

@login_required
def archive_habit(request, habit_id):
    if request.method != "POST":
        return redirect("habit_list")

    habit = get_object_or_404(Habit, pk=habit_id, user=request.user)
    habit.is_active = not habit.is_active
    habit.save()

    return redirect("habit_list")

@login_required
def delete_habit(request, habit_id):
    habit = get_object_or_404(Habit, pk=habit_id, user=request.user)

    if request.method == "POST":
        habit.delete()
        return redirect("habit_list")

    return render(request, "habits/habit_confirm_delete.html", {"habit": habit})

@login_required
def pause_list(request):
    pauses = Pause.objects.filter(user=request.user).order_by("-start_date")
    return render(request, "habits/pause_list.html", {"pauses": pauses})

@login_required
def create_pause(request):
    if request.method == "POST":
        form = PauseForm(request.POST)
        if form.is_valid():
            pause = form.save(commit=False)
            pause.user = request.user
            pause.save()
            return redirect("pause_list")
    else:
        form = PauseForm()

    return render(request, "habits/pause_form.html", {"form": form})

@login_required
def delete_pause(request, pause_id):
    pause = get_object_or_404(Pause, pk=pause_id, user=request.user)

    if request.method == "POST":
        pause.delete()
        return redirect("pause_list")
    return render(request, "habits/pause_confirm_delete.html", {"pause": pause})