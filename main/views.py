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
            email = form.cleaned_data.get("email")
            mate = form.cleaned_data.get("mate")
            if models.Notification.objects.filter(mate=mate, email=email).exists():
                messages.info(request, "This one already exists")
                return redirect("main:notification")
            form.save()
            messages.success(request, "Notification enabled")
            return redirect("main:index")
        else:
            messages.error(request, "Invalid input data")
    else:
        form = forms.NotificationForm()

    return render(request, "main/notification.html", {"form": form})


def unsubscribe(request):
    if request.method == "POST":
        form = forms.UnsubscribeForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            notifications = models.Notification.objects.filter(email=email)
            if notifications:
                notifications.delete()
                messages.info(request, "Email notification(s) deleted")
                return redirect("main:unsubscribe")
            else:
                messages.warning(request, "Email does not exist in notifications list")
                return redirect("main:unsubscribe")
        else:
            messages.error(request, "Invalid email")
    else:
        form = forms.UnsubscribeForm()

    return render(request, "main/unsubscribe.html", {"form": form})


def unsubscribe_oneclick(request, key):
    form = forms.UnsubscribeOneclickForm({"key": key})
    if form.is_valid():
        key = form.cleaned_data.get("key")
        notification = models.Notification.objects.filter(key=key)
        if notification:
            notification.delete()
            messages.success(request, "Unsubscribe successful")
        else:
            messages.error(request, "This email is not subscribed")
    else:
        messages.error(request, "Who are you?")

    return redirect("main:unsubscribe")
