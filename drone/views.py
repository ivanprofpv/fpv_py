from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.forms import inlineformset_factory
from django.http import HttpResponseNotFound
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from .forms import AddDroneForm, SignUpUserForm, LoginUserForm, AddComponentCategoryForm, \
    AddComponentForm, AddCommentForm, ProfileForm
from .utils import *
from .models import Profile

import logging

logger = logging.getLogger(__name__)

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
        return Drone.objects.filter(category__slug=self.kwargs['category_slug'], is_published=True).select_related('category')

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'].title)
        context['content'] = context['post'].content

        drone = self.object
        total_price = self.calculate_price(drone)
        context['total_price'] = total_price

        # Получение компонентов для текущего поста
        components = Component.objects.filter(drone=context['post'])
        context['components'] = components

        # Передаем форму комментариев
        form = AddCommentForm()
        context['form'] = form

        # Получаем комментарии
        comments = Comment.objects.filter(drone=context['post'], is_published=True)
        context['comments'] = comments

        # Получаем аватары комментаторов из их профилей (авторов комментариев)
        for comment in comments:
            user_avatar = Profile.objects.get(user=comment.author)
            context['avatars'] = user_avatar.avatar.url

        # Проверяем наличие лайка для юзера
        likes_connected = get_object_or_404(Drone, slug=self.kwargs['drone_slug'])
        liked = False
        if likes_connected.likes.filter(id=self.request.user.id).exists():
            liked = True

        # Передаем лайки в шаблон
        context['count_of_likes'] = likes_connected.count_of_likes()
        context['post_is_liked'] = liked

        return dict(list(context.items()) + list(c_def.items()))

    def post(self, request, *args, **kwargs):
        drone = self.get_object()
        form = AddCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            if request.user.is_authenticated:
                comment.author = request.user
                comment.drone = drone
                comment.save()
                return redirect('drone', drone_slug=drone.slug)
            else:
                return redirect('login')
        return self.render_to_response(self.get_context_data(form=form))

class CreatePost(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddDroneForm
    template_name = 'drone/add_drone.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        ComponentFormset = inlineformset_factory(Drone, Component, form=AddComponentForm, extra=3)
        if self.request.POST:
            context['components'] = ComponentFormset(self.request.POST)  # Создание формсета Component
        else:
            context['components'] = ComponentFormset()  # Пустой формсет Component

        c_def = self.get_user_context(title='Создание сборки')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        context = self.get_context_data()
        components = context['components']
        self.object = form.save(commit=False)
        self.object.author = self.request.user # Назначаем автора
        self.object.save()  # Сохранение экземпляра Drone

        if components.is_valid():
            components.instance = self.object
            components.save()  # Сохранение компонентов

        return super().form_valid(form)

class ComponentCategory(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddComponentCategoryForm
    template_name = 'drone/add_component_category.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Создание категории компонента')

        return dict(list(context.items()) + list(c_def.items()))

class SignUpUser(DataMixin, CreateView):
    form_class = SignUpUserForm
    template_name = 'drone/signup.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация')

        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)

        return redirect('home')

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

def DroneLike(request, slug):
    drone = get_object_or_404(Drone, slug=slug)
    if drone.likes.filter(id=request.user.id).exists():
        drone.likes.remove(request.user)
    else:
        drone.likes.add(request.user)

    return redirect(reverse('drone', kwargs={'drone_slug': slug}))

@login_required(login_url='login')
def profile(request):
    profile = request.user.profile
    user = request.user
    drone_count = Drone.objects.filter(author=user).count()
    comment_count = Comment.objects.filter(author=user).count()

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            # сохраняем данные из формы в профиле
            profile.email = form.cleaned_data['email']
            profile.bio = form.cleaned_data['bio']
            profile.avatar = form.cleaned_data['avatar']
            form.save()

            # сохраняем email и для самого пользователя
            user.email = profile.email
            user.save()

            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)

    context = {
        'form': form,
        'profile_avatar': profile.avatar.url,
        'bio': profile.bio,
        'drone_count': drone_count,
        'comment_count': comment_count,
    }

    return render(request, 'users/profile.html', context=context)