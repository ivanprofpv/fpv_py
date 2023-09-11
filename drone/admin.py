from django.contrib import admin

from .models import *

class DroneAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'time_create', 'drone_photo', 'is_published')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'time_create')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)

admin.site.register(Drone, DroneAdmin)
admin.site.register(Category, CategoryAdmin)