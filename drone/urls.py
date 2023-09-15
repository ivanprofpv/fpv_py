
from django.conf.urls.static import static
from django.urls import path

from buildfpv import settings
from .views import *

urlpatterns = [
    path('', DroneHome.as_view(), name='home'),
    path('drone/<slug:drone_slug>/', show_post, name='drone'),
    path('category/<slug:category_slug>/', show_category, name='category'),
    path('add/', add_drone, name='add_drone'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)