from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render

from .models import *

def show_post(request, drone_id):
    show_drone = Drone.objects.get(id=drone_id)
    return render(request, 'drone/details.html', {'post': show_drone})

def index(request):
    post = Drone.objects.all()
    return render(request, 'drone/index.html', {'post': post})
def pageNotFound(request, exception):
    return HttpResponseNotFound('Заглушка - страница не найдена (404)')