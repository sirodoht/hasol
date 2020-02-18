from django import forms

from main import models


class NotificationForm(forms.ModelForm):
    class Meta:
        model = models.Notification
        fields = ["email", "mate"]
        labels = {
            "email": "Email",
            "mate": "Who are you?",
        }
