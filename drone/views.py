from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from django.contrib import messages

from .models import *

def show_post(request, drone_id):
    show_drone = Drone.objects.get(id=drone_id)
    return render(request, 'drone/details.html', {'post': show_drone})

def index(request):
    post = Drone.objects.all()
    category = Category.objects.all()
    context = {
        'post': post,
        'category': category,
        'category_selected': 0,
    }
    return render(request, 'drone/index.html', context=context)
def pageNotFound(request, exception):
    return HttpResponseNotFound('Заглушка - страница не найдена (404)')

def show_category(request, category_id):
    category = Category.objects.all()
    post = Drone.objects.filter(category_id=category_id)

    if len(post) == 0:
        messages.info(request, 'Записи не найдены.')

    context = {
        'category': category,
        'post': post,
        'category_selected': category_id,
    }
    return render(request, 'drone/index.html', context=context)
