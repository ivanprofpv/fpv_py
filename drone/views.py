from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from django.contrib import messages

from .forms import AddDroneForm
from .models import *

class DroneHome(ListView):
    model = Drone
    template_name = 'drone/index.html'
    context_object_name = 'post'
    extra_context = {'title': 'Главная страница'}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        return context

    def get_queryset(self):
        return Drone.objects.filter(is_published=True)

def show_post(request, drone_slug):
    post = get_object_or_404(Drone, slug=drone_slug)
    context = {
        'post': post,
        'title': post.title,
        'content': post.content,
    }
    return render(request, 'drone/details.html', context=context)

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

def add_drone(request):
    if request.method == 'POST':
        form = AddDroneForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = AddDroneForm()
    return render(request, 'drone/add_drone.html', {'form': form, 'title': 'Создание сборки'})
