from django.shortcuts import render
from django.views.generic.detail import DetailView
from .models import StorageInfo, Client

# Create your views here.

class ClientDetail(DetailView):
    model = Client
    template_name = 'storage_info/client_info.html'


class StorageInfoDetail(DetailView):
    model = StorageInfo
    template_name = 'storage_info/storage_info.html'