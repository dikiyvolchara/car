from django.contrib import admin
from django.urls import path
from .views import Home, OlderRecords, TireDetail, OlderRecordsUpdate

app_name = 'tires'

urlpatterns = [
    path('old/update/', OlderRecordsUpdate, name="old_tire_update"),
    path('old/', OlderRecords, name="old_tire"),
    path('<str:slug>/', TireDetail, name='tire_detail'),
    path('', Home, name='new_tire'),
    #path('', Home.as_view(), name='new_tire'),
]