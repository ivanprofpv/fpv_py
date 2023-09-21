from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponseNotFound
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from .forms import AddDroneForm, SignUpUserForm, LoginUserForm
from .utils import *

class DroneHome(DataMixin, ListView):
    model = Drone
    template_name = 'drone/index.html'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Главная страница')
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Drone.objects.filter(is_published=True)

class DroneCategory(DataMixin, ListView):
    model = Drone
    template_name = 'drone/index.html'
    context_object_name = 'post'
    allow_empty = False

    def get_queryset(self):
        return Drone.objects.filter(category__slug=self.kwargs['category_slug'], is_published=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Категория ' + str(context['post'][0].category))
        context['category_selected'] = self.kwargs['category_slug'] #присваиваем значение текущей категории, переданной в url

        return dict(list(context.items()) + list(c_def.items()))

class ShowPost(DataMixin, DetailView):
    model = Drone
    template_name = 'drone/details.html'
    slug_url_kwarg = 'drone_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'].title)
        context['content'] = context['post'].content

        return dict(list(context.items()) + list(c_def.items()))

class CreatePost(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddDroneForm
    template_name = 'drone/add_drone.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Создание сборки')

        return dict(list(context.items()) + list(c_def.items()))

class SignUpUser(DataMixin, CreateView):
    form_class = SignUpUserForm
    template_name = 'drone/signup.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация')

        return dict(list(context.items()) + list(c_def.items()))

class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'drone/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Авторизация')

        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')

def pageNotFound(request, exception):
    return HttpResponseNotFound('Заглушка - страница не найдена (404)')

def logout_user(request):
    logout(request)
    return redirect('login')
