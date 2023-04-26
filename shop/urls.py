from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
	path('', views.index, name="index"),

    path('test/test', views.test, name='test'),

	path('contact', views.Contact, name="contact"),
	path('shynomontash-pogreby', views.Montash, name="montash"),

    path('shyny-bu-rozparovka', views.rozparovka, name='rozparovka'),
    path('shyny-bu-rozparovka/<str:category_slug>/', views.TireListByCategoryRozparovka, name='rozparovka-category'),
	
    path('<str:category_slug>/', views.TireListByCategory, name='category_list'),
	
    path('pdf/<int:id>/', views.render_pdf_detail_view, name='test-pdf-view'),
	path('pdf/category/<str:category_slug>/', views.render_pdf_category_view, name='category_pdf_list'),

    path('brand/<str:slug>/', views.BrandDetail, name='brand_detail'),

    path('<str:category_slug>/<str:slug>/', views.TireDetail, name='tire_detail'),
	
    path('brands/<str:brand_slug>/<str:slug>/', views.BrandModelDetail, name='brand_model_detail'),
	
]