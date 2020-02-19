from django.contrib import messages
from django.shortcuts import redirect, render

from main import forms, models


def index(request):
    return render(
        request,
        "main/index.html",
        {"assignments": models.Assignment.objects.filter(week="2020-02-17")},
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
