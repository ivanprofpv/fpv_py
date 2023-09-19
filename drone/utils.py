from .models import *

class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        category = Category.objects.all()
        context['category'] = category
        return context
