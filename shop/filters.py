import django_filters
from django import forms
from django.utils.translation import gettext as _

from .models import *

class UseTireFilter(django_filters.FilterSet):

    brand = django_filters.ModelMultipleChoiceFilter(
        label = 'Brand',
        field_name = 'model__brand__name',
        to_field_name = 'name',
        queryset = Brand.objects.all()
    )