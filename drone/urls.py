from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('drone/<int:drone_id>/', show_post, name='drone'),
    path('category/<int:category_id>/', show_category, name='category'),
]