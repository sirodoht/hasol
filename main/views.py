from django.shortcuts import render


def index(request):
    return render('main/index.html')
