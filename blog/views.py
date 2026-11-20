from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return HttpResponse(
        "<h1>Блог с рубриками</h1>"
        "<p>Добро пожаловать на сайт!</p>"
    )