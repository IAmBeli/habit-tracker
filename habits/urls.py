from django.urls import path
from . import views

urlpatterns = [
    path("", views.today, name="today"),
    path("habits/<int:habit_id>/toggle/", views.toggle, name="toggle"),
    path("habits/new/", views.create_habit, name="create_habit"),
    path("habits/", views.habit_list, name="habit_list"),
    path("habits/<int:habit_id>/archive/", views.archive_habit, name="archive_habit"),
    path("habits/<int:habit_id>/delete/", views.delete_habit, name="delete_habit"),
    path("pauses/", views.pause_list, name="pause_list"),
    path("pauses/new/", views.create_pause, name="create_pause"),
    path("pauses/<int:pause_id>/delete/", views.delete_pause, name="delete_pause"),
]