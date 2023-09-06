from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('drone/<int:pk>/', DroneDetailsView.as_view(), name='drone-detail'),
]