from django.db.models import Sum

from .models import *

class DataMixin:
    paginate_by = 3
    def get_user_context(self, **kwargs):
        context = kwargs
        category = Category.objects.all()
        context['category'] = category
        return context

    def calculate_price(self, drone):
        total_price = Component.objects.filter(drone=drone).aggregate(total_price=Sum('price'))['total_price']
        return total_price