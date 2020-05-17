import uuid

from django.db import models
from django.utils import timezone


class Mate(models.Model):
    name = models.CharField(max_length=300)
    joined_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class Job(models.Model):
    title = models.CharField(max_length=300)
    created_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Assignment(models.Model):
    mate = models.ForeignKey(Mate, null=True, on_delete=models.SET_NULL)
    job = models.ForeignKey(Job, null=True, on_delete=models.SET_NULL)
    week_start = models.DateField(default=timezone.now)

    def __str__(self):
        return (
            self.week_start.isoformat() + ": " + self.mate.name + " – " + self.job.title
        )


class Notification(models.Model):
    email = models.EmailField()
    key = models.UUIDField(default=uuid.uuid4)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.email + " – " + str(self.key)


class NotificationSent(models.Model):
    notification = models.ForeignKey(Notification, on_delete=models.SET_NULL, null=True)
    sent_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.sent_at + " – " + self.notification.email


class Todo(models.Model):
    body = models.CharField(max_length=500)
    created_at = models.DateTimeField(default=timezone.now)
    completed_at = models.DateTimeField(default=None, null=True)

    def __str__(self):
        return self.body
