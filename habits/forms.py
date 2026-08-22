from django import forms
from .models import Habit

class HabitForm(forms.ModelForm):
    class Meta:
        model = Habit
        fields = ["title", "start_date", "interval_days"]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"})
        }