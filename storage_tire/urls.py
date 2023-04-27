from django.urls import path
from .views import StorageInfoDetail, ClientDetail

app_name = 'storage_info'

urlpatterns = [
	path('<str:client_slug>/<str:slug>/', StorageInfoDetail.as_view(), name="detail_storage_info"),
    path('<str:slug>/', ClientDetail.as_view(), name='client_storage_info')
]