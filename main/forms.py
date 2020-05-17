from django import forms

from main import models


class NotificationForm(forms.ModelForm):
    class Meta:
        model = models.Notification
        fields = ["email"]


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


class TodoForm(forms.ModelForm):
    class Meta:
        model = models.Todo
        fields = ["body"]
        labels = {
            "body": "Add a new to-do item",
        }


class WriteForm(forms.Form):
    body = forms.CharField(widget=forms.Textarea)
    dryrun = forms.BooleanField(required=False)
