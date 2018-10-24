from django.urls import path

from . import views

app_name = "reports"

urlpatterns = [
    path("day/", views.view_day, name="day"),
    path("week/", views.view_week, name="week"),
    path("month/", views.view_month, name="month"),
]
