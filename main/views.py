from django.shortcuts import render

from main import models


def index(request):
    return render(
        request, "main/index.html", {"assignments": models.Assignment.objects.all()}
    )
