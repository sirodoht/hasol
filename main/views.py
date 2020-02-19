from datetime import datetime, timedelta

from django.contrib import messages
from django.shortcuts import redirect, render

from main import forms, models


def index(request):
    now = datetime.now()
    monday_this_week = now - timedelta(days=now.weekday())
    return render(
        request,
        "main/index.html",
        {"assignments": models.Assignment.objects.filter(week_start=monday_this_week)},
    )


def notification(request):
    if request.method == "POST":
        form = forms.NotificationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Notification enabled")
            return redirect("main:index")
        else:
            messages.error(request, "Invalid password.")
    else:
        form = forms.NotificationForm()

    return render(request, "main/notification.html", {"form": form})
