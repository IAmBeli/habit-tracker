from django.contrib import admin
from .models import Habit, Completion, Pause

admin.site.register(Habit)
admin.site.register(Completion)
admin.site.register(Pause)