from django import forms
from .models import *

class AddDroneForm(forms.Form):
    title = forms.CharField(max_length=255)
    slug = forms.SlugField(max_length=255)
    content = forms.CharField
    #drone_photo = forms.ImageField(upload_to="photos/%Y/%m/%d")
    is_published = forms.BooleanField()
    category = forms.ModelChoiceField(queryset=Category.objects.all())