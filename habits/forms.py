from django import forms
from .models import Habit, Pause

class HabitForm(forms.ModelForm):
    class Meta:
        model = Habit
        fields = ["title", "start_date", "interval_days"]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"})
        }

class PauseForm(forms.ModelForm):
    class Meta:
        model = Pause
        fields = ["start_date", "end_date", "reason"]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }
    def clean(self):
        cleaned = super().clean()
        start = cleaned.get("start_date")
        end = cleaned.get("end_date")

        if start and end and end < start:
            raise forms.ValidationError("End date cannot be before start date")

        return cleaned