from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from django.contrib import messages

from .models import *

def show_post(request, drone_slug):
    post = get_object_or_404(Drone, slug=drone_slug)
    context = {
        'post': post,
        'title': post.title,
        'content': post.content,
    }
    return render(request, 'drone/details.html', context=context)

def index(request):
    post = Drone.objects.all()
    context = {
        'post': post,
    }
    return render(request, 'drone/index.html', context=context)
def pageNotFound(request, exception):
    return HttpResponseNotFound('Заглушка - страница не найдена (404)')

def show_category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    post = Drone.objects.filter(category=category)

    if len(post) == 0:
        messages.info(request, 'Записи не найдены.')

    context = {
        'post': post,
        'category_selected': category_slug,
    }
    return render(request, 'drone/index.html', context=context)
