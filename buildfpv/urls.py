from django.contrib import admin
from django.urls import path, include
from drone.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('drone.urls'))
]

handler404 = pageNotFound