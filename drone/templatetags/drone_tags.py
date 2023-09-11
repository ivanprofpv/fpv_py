from django import template
from drone.models import *

register = template.Library()

#simple_tag декоратор экземпляра класса Library
@register.simple_tag()
def get_categories():
    return Category.objects.all()