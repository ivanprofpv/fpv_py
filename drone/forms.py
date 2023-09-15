from django import forms
from django.core.exceptions import ValidationError

from .models import *

class AddDroneForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = 'Выберите категорию'
    class Meta:
        model = Drone
        fields = ['title', 'drone_photo', 'content', 'is_published', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select form-select'}),
            'drone_photo': forms.ClearableFileInput(attrs={'class': 'form-control'})
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 200:
            raise ValidationError('Длина превышает 200 символов!')

        return title

    def clean_content(self):
        content = self.cleaned_data['content']
        if len(content) > 50000:
            raise ValidationError('Длина превышает 50000 символов!')

        return content