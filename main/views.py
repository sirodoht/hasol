import json
import uuid
from datetime import datetime, timedelta

from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import mail_admins, send_mail
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt

from hasol import settings
from main import forms, models


def index(request):
    # calculate today's week
    now = datetime.now().date()
    monday_this_week = now - timedelta(days=now.weekday())

    # calculate next and previous weeks to the one requested
    previous_monday = monday_this_week - timedelta(days=7)
    next_monday = monday_this_week + timedelta(days=7)

    return render(
        request,
        "main/index.html",
        {
            "assignments": models.Assignment.objects.filter(
                week_start=monday_this_week
            ),
            "is_todays": True,
            "current": monday_this_week,
            "current_endweek": monday_this_week + timedelta(days=6),
            "previous": previous_monday,
            "next": next_monday,
        },
    )


def rota(request, isodate):
    # calculate today's week
    now = datetime.now().date()
    monday_this_week = now - timedelta(days=now.weekday())

    # calculate requested week
    date_requested = datetime.strptime(isodate, "%Y-%m-%d").date()
    monday_that_week = date_requested - timedelta(days=date_requested.weekday())

    # if date is not a Monday, redirect to the Monday of that week
    if date_requested.weekday() != 0:
        return redirect("main:rota", isodate=monday_that_week.date())

    # calculate next and previous weeks to the one requested
    previous_monday = monday_that_week - timedelta(days=7)
    next_monday = monday_that_week + timedelta(days=7)

    return render(
        request,
        "main/index.html",
        {
            "assignments": models.Assignment.objects.filter(
                week_start=monday_that_week
            ),
            "is_todays": monday_this_week == monday_that_week,
            "todays": monday_this_week,
            "current": monday_that_week,
            "current_endweek": monday_that_week + timedelta(days=6),
            "previous": previous_monday,
            "next": next_monday,
        },
    )


def notification(request):
    if request.method == "POST":
        form = forms.NotificationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            if models.Notification.objects.filter(email=email).exists():
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


@csrf_exempt
def announce(request):
    if request.method == "POST":
        # hardcoded authentication
        body = request.body.decode("utf-8")
        data = json.loads(body)
        if data.get("key") != "gooHa4o":
            return JsonResponse(status=403, data={})

        # calculate today's week
        now = datetime.now().date()
        monday_this_week = now - timedelta(days=now.weekday())

        # product email content
        this_week_assignments = models.Assignment.objects.filter(
            week_start=monday_this_week
        )
        rota_content = ""
        for a in this_week_assignments:
            rota_content += a.mate.name + " — " + a.job.title + "\n"

        # handle dry run case
        if data.get("dryrun"):
            mail_admins(
                "Nutcroft is clean!",
                render_to_string(
                    "main/rota_announce_email.txt",
                    {
                        "domain": get_current_site(request).domain,
                        "rota": rota_content,
                        "key": uuid.uuid4(),
                    },
                    request=request,
                ),
            )
            return JsonResponse(status=200, data={})

        # sent notifications
        for n in models.Notification.objects.all():
            send_mail(
                "Nutcroft is clean!",
                render_to_string(
                    "main/rota_announce_email.txt",
                    {
                        "domain": get_current_site(request).domain,
                        "rota": rota_content,
                        "key": n.key,
                    },
                    request=request,
                ),
                settings.DEFAULT_FROM_EMAIL,
                [n.email],
            )
            models.NotificationSent.objects.create(notification=n)

    return JsonResponse(status=200, data={})


def todo(request):
    todos = models.Todo.objects.filter(completed_at=None)
    done_todos = models.Todo.objects.filter(completed_at__isnull=False).order_by(
        "-completed_at"
    )
    if request.method == "POST":
        form = forms.TodoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "To do saved.")
            return redirect("main:todo")
        else:
            messages.error(request, "Invalid input data")
    else:
        form = forms.TodoForm()

    return render(
        request,
        "main/todo.html",
        {"form": form, "todos": todos, "done_todos": done_todos},
    )


def todo_delete(request, todo_id):
    if request.method == "POST":
        todo = models.Todo.objects.get(id=todo_id)
        todo.completed_at = datetime.now()
        todo.save()
        return JsonResponse(status=200, data={})


def constitution(request):
    return render(request, "main/constitution.html")


def garden(request):
    return render(request, "main/garden.html")
