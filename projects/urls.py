from django.urls import path

from . import views

app_name = "projects"

urlpatterns = [
    path("list/", views.list_view, name="list"),
    path("create/", views.create_view, name="create"),
    path("edit/<slug>/", views.edit_view, name="edit"),
    path("archive/<slug>/", views.archive_view, name="archive"),
    path("delete/<slug>/", views.delete_view, name="delete"),
]
