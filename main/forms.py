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


class UnsubscribeForm(forms.ModelForm):
    class Meta:
        model = models.Notification
        fields = ["email"]
        labels = {
            "email": "Email to be deleted from notifications",
        }


class UnsubscribeOneclickForm(forms.ModelForm):
    class Meta:
        model = models.Notification
        fields = ["key"]
