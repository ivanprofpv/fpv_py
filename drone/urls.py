from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('drone/<slug:drone_slug>/', show_post, name='drone'),
    path('category/<slug:category_slug>/', show_category, name='category'),
    path('add/', add_drone, name='add_drone'),
]