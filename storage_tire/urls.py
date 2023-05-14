from django.urls import path
from .views import StorageInfoDetail, ClientDetail
from . import views

app_name = 'storage_info'

urlpatterns = [
    path('pdf/<int:id>/', views.render_pdf_storage_info, name='pdf-storage-info'),
	path('<str:client_slug>/<str:slug>/', StorageInfoDetail.as_view(), name="detail_storage_info"),
    path('<str:slug>/', ClientDetail.as_view(), name='client_storage_info')
]