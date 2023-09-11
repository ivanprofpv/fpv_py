from django import template
from drone.models import *

register = template.Library()
@register.inclusion_tag('drone/tags/list_categories.html')
def show_categories(category_selected=0):
    category = Category.objects.all()
    return {"category": category, 'category_selected': category_selected}