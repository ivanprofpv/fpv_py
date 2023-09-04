from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return HttpResponse("заглушка")

def show(request, droneid):
    return HttpResponse("заглушка карточки")
