import django_filters
from django import forms

from .models import *

class TireFilter(django_filters.FilterSet):

    CHOICES = (
        ('expensive', 'Дорожчі'),
        ('cheap', 'Дешевші')
    )

    ordering = django_filters.ChoiceFilter(label='Сортувати:', choices=CHOICES, method='filter_by_order')


    brand = django_filters.ModelMultipleChoiceFilter(
        label='Бренд',
        field_name='brand__name',
        to_field_name='name',
        queryset=Brand.objects.all(),
    )

    width = django_filters.ModelMultipleChoiceFilter(
        label='Ширина',
        field_name='width__name',
        to_field_name='name',
        queryset=Width.objects.all(),
    )

    height = django_filters.ModelMultipleChoiceFilter(
        label='Висота',
        field_name='height__name',
        to_field_name='name',
        queryset=Height.objects.all(),
    )

    radius = django_filters.ModelMultipleChoiceFilter(
        label='Радіус',
        field_name='radius__name',
        to_field_name='name',
        queryset=Radius.objects.all(),
    )

    season = django_filters.ModelMultipleChoiceFilter(
        label='Сезон',
        field_name='season__name',
        to_field_name='name',
        queryset=Season.objects.all(),
    )

    kind = django_filters.ModelMultipleChoiceFilter(
        label='Тип',
        field_name='kind__name',
        to_field_name='name',
        queryset=Kind.objects.all(),
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