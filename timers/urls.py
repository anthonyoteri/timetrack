from django.urls import path

from . import views

app_name = "timers"

urlpatterns = [
    path("list/", views.list_view, name="list"),
    path("edit/<int:id>/", views.edit_view, name="edit"),
    path("create/", views.create_view, name="create"),
    path("delete/<int:id>/", views.delete_view, name="delete"),
    path("stop/<int:id>/", views.stop_view, name="stop"),
    path("start/<slug>/", views.start_view, name="start"),
]
