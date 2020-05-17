from django.contrib import admin
from django.urls import path, re_path

from main import views

admin.site.site_header = "hasol administration"
app_name = "main"

urlpatterns = [
    path("", views.index, name="index"),
    re_path(r"^rota/(?P<isodate>\d{4}-\d{2}-\d{2})/$", views.rota, name="rota"),
    path("notification/", views.notification, name="notification"),
    path("unsubscribe/", views.unsubscribe, name="unsubscribe"),
    path(
        "unsubscribe/<uuid:key>",
        views.unsubscribe_oneclick,
        name="unsubscribe_oneclick",
    ),
    path("write/", views.write, name="write"),
    path("announce/", views.announce, name="announce"),
    path("todo/", views.todo, name="todo"),
    path("todo/<int:todo_id>/delete/", views.todo_delete, name="todo_delete"),
    path("constitution/", views.constitution, name="constitution"),
    path("garden/", views.garden, name="garden"),
    path("bet/", views.bet, name="bet"),
]
