from django.contrib import admin

from .models import *

class DroneAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'time_create', 'drone_photo', 'is_published')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'time_create')
    prepopulated_fields = {'slug': ('title',)}

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

class ComponentCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}

class CommentCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'content', 'drone', 'author', 'is_published')
    list_display_links = ('id', 'content')
    search_fields = ('content',)
    list_editable = ('is_published',)

admin.site.register(Drone, DroneAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(ComponentCategory, ComponentCategoryAdmin)
admin.site.register(Comment, CommentCategoryAdmin)