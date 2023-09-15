from django.http import HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView

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

class DroneCategory(ListView):
    model = Drone
    template_name = 'drone/index.html'
    context_object_name = 'post'
    allow_empty = False

    def get_queryset(self):
        return Drone.objects.filter(category__slug=self.kwargs['category_slug'], is_published=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Категория ' + str(context['post'][0].category)
        context['category_selected'] = self.kwargs['category_slug'] #присваиваем значение текущей категории, переданной в url

        return context

class ShowPost(DetailView):
    model = Drone
    template_name = 'drone/details.html'
    slug_url_kwarg = 'drone_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = str(context['post'].title)
        context['content'] = str(context['post'].content)

        return context

def pageNotFound(request, exception):
    return HttpResponseNotFound('Заглушка - страница не найдена (404)')

def add_drone(request):
    if request.method == 'POST':
        form = AddDroneForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = AddDroneForm()
    return render(request, 'drone/add_drone.html', {'form': form, 'title': 'Создание сборки'})
