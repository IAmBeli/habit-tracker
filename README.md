# habit-tracker

A Django application for tracking recurring personal goals — review flashcards every day, go to the gym every third day — with streaks, a month calendar, and pauses that freeze a streak instead of breaking it.

This is a personal tool first and a portfolio project second. The features exist because I wanted them, which is also why the awkward parts got solved rather than avoided.

## What it does

The main page lists what is due today and nothing else. Marking something done is one button, and pressing it again undoes it — mistakes should be cheap to fix.

The calendar shows a month at a glance, each day coloured by whether everything, some, or none of that day's habits were completed. Pauses appear in their own colour.

Pauses are the part I care about most. Being ill for a week should not destroy a three-month streak, but it should not silently count as success either. A pause freezes the streak: those days are skipped rather than counted or held against you.

## How scheduling works

A habit is defined by a start date and an interval. Due dates are computed from the start date, not from the last completion:

```
start 1 August, interval 3  →  due on 1, 4, 7, 10 August...
```

Missing the 4th does not shift the 7th. This keeps the schedule predictable, and it means a habit's due dates can be computed for any date without looking at history.

The alternative — next due date equals last completion plus interval — is a reasonable design too, and better for things where the gap matters more than the calendar. Adding it later would mean one field on the model and a branch in one function.

## Streaks are computed, not stored

There is no `streak` column anywhere. The database stores events — one row per completion, one row per pause — and streaks are derived from them on every request.

This costs a little computation and buys quite a lot. A mis-clicked completion can be undone and the streak corrects itself. A pause can be deleted and every streak recalculates without a migration or a repair script. History stays intact when a habit is archived.

The general rule this follows: store what happened, derive the summary. The reverse — storing a running total and updating it — is faster to read and much harder to fix once it drifts.

## Timezones

The whole application hinges on what "today" means, so a single global `TIME_ZONE` was not enough. Each user has a `Profile` with their own timezone, and a middleware activates it on every request before any view asks for the current date.

Without this, a user twelve hours from the server would be told they had missed habits they still had all evening to do. Handling it needed a one-to-one model, a middleware, and `choices` populated from `zoneinfo` so the value cannot be a typo.

## Privacy

Every query that touches user data filters by owner at the database level:

```python
Habit.objects.filter(user=request.user)
get_object_or_404(Habit, pk=habit_id, user=request.user)
```

The second one matters more than it looks. Habit IDs are sequential and sit in plain view in the URL, so anyone signed in could type someone else's number. Because the ownership check is part of the lookup rather than a separate `if`, a habit that is not yours simply is not found, and the request returns 404 without confirming the record exists.

Two tests cover exactly this: another user does not see your habits, and cannot toggle them by ID.

## Project layout

```
config/          settings, root URL table, timezone middleware registration
habits/
    models.py        Habit, Completion, Pause, Profile
    services.py      pure scheduling logic — no database, no Django
    selectors.py     database reads shared between views
    forms.py         HabitForm, PauseForm, ProfileForm
    views.py         request handling
    middleware.py    activates the user's timezone
    tests/           pytest suite
    templates/
    static/
```

`services.py` is deliberately isolated. `is_due`, `current_streak`, `paused_days` and `month_summary` take dates and sets and return dates and numbers — they know nothing about models or requests. That makes them testable in isolation, and the whole test suite for them runs without a database.

## Tests

```bash
pytest
```

The scheduling tests cover boundaries rather than happy paths, because that is where this kind of code breaks. One of them exists because of a real bug: `paused_days` used a strict `<`, so a pause where the start and end dates were the same produced an empty set and had no effect at all. A multi-day pause merely lost its last day, which is easy to miss; the single-day case failed completely, which is how it was noticed.

The view tests cover authentication, ownership, and the toggle behaviour.

## Getting started

### 1. Database

```bash
docker run --name habits-db \
  -e POSTGRES_USER=habits \
  -e POSTGRES_PASSWORD=<your password> \
  -e POSTGRES_DB=habitsdb \
  -p 5433:5432 \
  --restart unless-stopped \
  -d postgres:16
```

Port 5433 on the host, to avoid colliding with another Postgres container.

### 2. Configuration

Copy `.env.example` to `.env` and fill it in. `.env` is git-ignored; `.env.example` documents the required variables without exposing values.

### 3. Run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Requires Python 3.10 or newer.

## Possible extensions

- Rolling schedules alongside fixed ones, chosen per habit
- Editing a habit after creation — the form already supports it via `instance=`
- Photo proof attached to a completion
- Deployment, so it is usable from a phone rather than only on localhost

## License

MIT