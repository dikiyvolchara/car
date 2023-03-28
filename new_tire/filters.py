import django_filters
from django import forms

from .models import *

class TireFilter(django_filters.FilterSet):

    CHOICES = (
        ('expensive', 'Дорожчі'),
        ('cheap', 'Дешевші')
    )

    ordering = django_filters.ChoiceFilter(label='Сортувати:', choices=CHOICES, method='filter_by_order')
    width = django_filters.filters.ModelMultipleChoiceFilter(
        label='Ширина',
        field_name='width__name',
        to_field_name='name',
        queryset=Width.objects.all(),
    )
    


    def filter_by_order(self, queryset, name, value):
        expression = '-price_two' if value == 'expensive' else 'price_two'
        return queryset.order_by(expression)
        
    class Meta:
        model = Tire
        
        # fields = ('brand', 'width', 'height', 'radius', 'kind', 'season')
        fields = {
            'price_two': ['gt', 'lt'],
            # 'brand': ['exact', ],
            # 'width': ['exact', ],
            # 'height': ['exact', ],
            # 'radius': ['exact', ],
        }