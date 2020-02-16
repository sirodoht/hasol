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

    def __str__(self):
        return self.title


class Assignment(models.Model):
    mate = models.ForeignKey(Mate, null=True, on_delete=models.SET_NULL)
    job = models.ForeignKey(Job, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.mate.name + " - " + self.job.title
