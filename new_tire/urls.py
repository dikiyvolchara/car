from django.contrib import admin
from django.urls import path
from .views import Home, TireDetail, UpdatePrice

app_name = 'tires'

urlpatterns = [
    path('update-price/update', UpdatePrice, name="update_price"),
    path('<str:slug>/', TireDetail, name='tire_detail'),
    path('', Home, name='new_tire'),
    #path('', Home.as_view(), name='new_tire'),
]