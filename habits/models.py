from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator

class Habit(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="habits",
    )
    title = models.CharField(max_length=200)
    start_date = models.DateField()
    interval_days = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(interval_days__gte=1),
                name="intervals_at_least_one",
            ),
        ]

    def __str__(self):
        return self.title

class Completion(models.Model):
    habit = models.ForeignKey(
        Habit,
        on_delete=models.CASCADE,
        related_name="completions",
    )
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["habit", "date"], name="unique_habit_date"),
        ]

    def __str__(self):
        return f"{self.habit.title} on {self.date}"

class Pause(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="pauses",
    )
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.CharField(max_length=300)

    def __str__(self):
        return f"{self.start_date} - {self.end_date}"