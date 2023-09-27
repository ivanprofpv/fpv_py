
from django.conf.urls.static import static
from django.urls import path, include

from buildfpv import settings
from .views import *

urlpatterns = [
    path('', DroneHome.as_view(), name='home'),
    path('drone/<slug:drone_slug>/', ShowPost.as_view(), name='drone'),
    path('category/<slug:category_slug>/', DroneCategory.as_view(), name='category'),
    path('component_category/<slug:component_category_slug>/', ComponentCategory.as_view(), name='component_category'),
    path('add/', CreatePost.as_view(), name='add_drone'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('signup/', SignUpUser.as_view(), name='signup'),
    path('tinymce/', include('tinymce.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)