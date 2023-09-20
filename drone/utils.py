from .models import *

class DataMixin:
    paginate_by = 3
    def get_user_context(self, **kwargs):
        context = kwargs
        category = Category.objects.all()
        context['category'] = category
        return context
