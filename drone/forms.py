from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from tinymce.widgets import TinyMCE

from .models import *

class AddComponentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['component_category'].empty_label = 'Выберите компонент'
    class Meta:
        model = Component
        fields = ['component_category', 'name', 'url', 'price']
        widgets = {
            'drone': forms.HiddenInput(),
            'component_category': forms.Select(attrs={'class': 'form-select form-select'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название компонента'}),
            'url': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ссылка'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Цена'}),
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) > 100:
            raise ValidationError('Максимальная длина названия не должна превышать 100 символов.')

        return name

class AddDroneForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = 'Выберите категорию дрона'
    class Meta:
        model = Drone
        fields = ['title', 'drone_photo', 'content', 'is_published', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-input'}),
            'content': TinyMCE(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select form-select'}),
            'drone_photo': forms.ClearableFileInput(attrs={'class': 'form-control'})
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 200:
            raise ValidationError('Максимальная длина заголовка не должна превышать 200 символов.')

        return title

    def clean_content(self):
        content = self.cleaned_data['content']
        if len(content) > 50000:
            raise ValidationError('Длина статьи превышает 50000 символов.')

        return content

class AddComponentCategoryForm(forms.ModelForm):
    class Meta:
        model = ComponentCategory
        fields = ['title']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-input'}),
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 100:
            raise ValidationError('Длина названия превышает 100 символов.')

        return title

class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Напишите комментарий'}),
        }

    def clean_content(self):
        content = self.cleaned_data['content']
        if len(content) > 255:
            raise ValidationError('Длина комментария превышает 255 символов.')

        return content

class SignUpUserForm(UserCreationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.CharField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'password1'}))
    password2 = forms.CharField(label='Подтвердите пароль', widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'password2'}))
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с таким email уже существует.')

        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        if len(username) > 30:
            raise ValidationError('Максимальная длина имени пользователя - 30 символов.')

        return username

class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))