from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from django.views.generic import DetailView

from .models import *

class DroneDetailsView(DetailView):
    model = Drone
    template_name = 'drone/details.html'
    context_object_name = 'drone'

def index(request):
    post = Drone.objects.all()
    return render(request, 'drone/index.html', {'post': post})

def details(request, droneid):
    return render(request, 'drone/details.html')

def pageNotFound(request, exception):
    return HttpResponseNotFound('Заглушка - страница не найдена (404)')