from django.urls import path

from . import views

app_name = "backup"

urlpatterns = [
    path("", views.index_view, name="index"),
    path("backup/", views.backup_view, name="backup"),
    path("restore/", views.restore_view, name="restore"),
]
