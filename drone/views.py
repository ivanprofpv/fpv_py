from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render

def index(request):
    return HttpResponse("заглушка")

def show(request, droneid):
    return HttpResponse("заглушка карточки")

def pageNotFound(request, exception):
    return HttpResponseNotFound('Заглушка - страница не найдена (404)')