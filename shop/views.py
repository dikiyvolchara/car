import requests
import datetime
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from itertools import groupby
from django.template import loader
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages
from .models import *
from .forms import QuickOrderForm
from django.core.validators import MinValueValidator, MaxValueValidator

#xhtml2pdf import packe
from django.template.loader import get_template
from xhtml2pdf import pisa


# Create your views here.
def index(request):

    template = loader.get_template('shop/index.html')

    popular_tires = Tire.objects.filter(available=True)[:6]

    category = Category.objects.filter(tire_category__available=True, tire_category__in_stock__gte=2)

    
    category = [cat for cat, _ in groupby(category)]

    category_dict_count = {}
    for cat in category:
        cat_count = Category.objects.filter(
            name=cat.name, tire_category__available=True, tire_category__in_stock__gte=2).count()
        category_dict_count[cat.name] = cat_count

    radius = []

    for cat in category:
        if cat.name[7:10] not in radius:
            radius.append(cat.name[7:10])
    radius.sort()

    description_index = Brand.objects.get(name='index')
    brands = set(Brand.objects.filter(brand_model__tire_model__available=True))


    # func to wheather API
   
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&lang=uk&cnt=3&appid=596d0ac48c27ba6317ac02395662571c&units=metric'
    city = 'Kyiv'
    city_weather = requests.get(url.format(city)).json()
    weather = {
        'city' : city,
        'temperature' : city_weather['main']['temp'],
        'min': city_weather['main']['temp_min'],
        'max': city_weather['main']['temp_max'],
        'feels_like': city_weather['main']['feels_like'],
        'description' : city_weather['weather'][0]['description'],
        'background': city_weather['weather'][0]['main'],
        'icon' : city_weather['weather'][0]['icon'],
    }

    context = {
        'category': category,
        'radius': radius,
        'category_dict_count': category_dict_count,
        'brands': brands,
        'popular_tires': popular_tires,
        'description_index': description_index,
        'weather': weather,
    }

    return HttpResponse(template.render(context, request))


def TireListByCategory(request, category_slug):
    template = loader.get_template('shop/category.html')
    category = get_object_or_404(Category, slug=category_slug)

    tires = Tire.objects.filter(category=category, in_stock__gte=2).order_by('-available', 'price')

    paginator = Paginator(tires, 25) # Show 25 contacts per page.

    page_number = request.GET.get('page')
    tires_obj = paginator.get_page(page_number)

    context = {
        'category': category,
        'tires': tires,
        'tires_obj': tires_obj,
    }

    return HttpResponse(template.render(context, request))


# Rozparovka.
def rozparovka(request):

    template = loader.get_template('shop/rozparovka.html')

    category = Category.objects.filter(tire_category__available=True, tire_category__in_stock__lte=1)
 
    category = [cat for cat, _ in groupby(category)]

    category_dict_count = {}
    for cat in category:
        cat_count = Category.objects.filter(
            name=cat.name, tire_category__available=True, tire_category__in_stock__lte=1).count()
        category_dict_count[cat.name] = cat_count

    radius = []

    for cat in category:
        if cat.name[7:10] not in radius:
            radius.append(cat.name[7:10])
    radius.sort()

    context = {
        'category': category,
        'radius': radius,
        'category_dict_count': category_dict_count,
    }

    return HttpResponse(template.render(context, request))




def TireListByCategoryRozparovka(request, category_slug):
    template = loader.get_template('shop/rozparovka-category.html')
    category = get_object_or_404(Category, slug=category_slug)

    tires = Tire.objects.filter(category=category, available=True, in_stock__lte=1).order_by('price')

    context = {
        'category': category,
        'tires': tires,
    }

    return HttpResponse(template.render(context, request))



def TireDetail(request, category_slug, slug):

    template = loader.get_template('shop/detail.html')

    tire = get_object_or_404(Tire, category__slug=category_slug, slug=slug)

    same_tires = Tire.objects.filter(category=tire.category, available=True)
    
    if request.method == 'POST':
        form = QuickOrderForm(request.POST)
        
        #form.fields['phone'].validators = [MinValueValidator(500000000, message='Не вистачає цифри. Приклад: 0971234455'),
        #                                   MaxValueValidator(999999999, message='Ви вели забагато цифр. Приклад: 0971234455')]

        if form.is_valid():
            qo = form.save(commit=False)
            try:
                QuickOrder.objects.get(phone=qo.phone, tire=tire)
                messages.success(request, "Ваше замовлення отримано менеджером. Чекайте на дзвінок.")
            except QuickOrder.DoesNotExist:
                if request.user.username == 'AnonymouseUser':
                        
                    obj, create = QuickOrder.objects.update_or_create(phone=qo.phone, tire=tire, price=tire.price)
                    messages.success(request, "Дякуємо! Заявка надіслана успішно! Скоро з Вами зв'яжеться наш менеджер.")
                else:
                    
                    obj, create = QuickOrder.objects.update_or_create(phone=qo.phone, tire=tire, price=tire.price, client=request.user)
                    messages.success(request, "Дякуємо! Заявка надіслана успішно! Скоро з Вами зв'яжеться наш менеджер.")
    else:
        form = QuickOrderForm()

    context = {
        'tire': tire,
        'same_tires': same_tires,
        'form': form,
    }

    return HttpResponse(template.render(context, request))

def BrandDetail(request, slug):

    template = loader.get_template('shop/brand_detail.html')

    brand = get_object_or_404(Brand, slug=slug)

    brand_models = BrandModel.objects.filter(brand=brand)

    tires = Tire.objects.filter(model__brand=brand).order_by('-available')

    paginator = Paginator(tires, 15)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    context = {
        'brand': brand,
        'page_obj': page_obj,
        'brand_models': brand_models,
    }

    return HttpResponse(template.render(context, request))


def BrandModelDetail(request, brand_slug, slug):

    template = loader.get_template('shop/brand_model_detail.html')

    brand_model = get_object_or_404(BrandModel, brand__slug=brand_slug, slug=slug)

    tires = Tire.objects.filter(model=brand_model).order_by('-available')

    context = {
        'brand_model': brand_model,
        'tires': tires,
    }

    return HttpResponse(template.render(context, request))

#contact view inform
def Contact(request):

    template = loader.get_template('shop/contact.html')

    context = {
    }

    return HttpResponse(template.render(context, request))


#montash view inform
def Montash(request):

    template = loader.get_template('shop/montash.html')

    context = {
    }

    return HttpResponse(template.render(context, request))

#render html to pdf
def render_pdf_detail_view(request, id):
    if request.user.is_authenticated:
        tire = get_object_or_404(Tire, id=id)

        template_path = 'shop/detail-pdf.html'


        context = {'tire': tire}
        # Create a Django response object, and specify content_type as pdf
        response = HttpResponse(content_type='application/pdf')

        #if download:
        #response['Content-Disposition'] = 'attachment; filename="qr-code.pdf"'

        #if display:
        response['Content-Disposition'] = 'filename="qr-code.pdf"'

        # find the template and render it.
        template = get_template(template_path)
        html = template.render(context)

        # create a pdf
        pisa_status = pisa.CreatePDF(
        html, dest=response)
        # if error then show some funny view
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response
    else:
        return redirect('https://car-plus.kyiv.ua')
    # return HttpResponse(template.render(context, request))

    
#render html to pdf
def render_pdf_category_view(request, category_slug):

    if request.user.is_authenticated:

        category = get_object_or_404(Category, slug=category_slug)

        tires = Tire.objects.filter(category=category, available=True).order_by('price')

        template_path = 'shop/category-pdf.html'


        context = {'tires': tires}
        # Create a Django response object, and specify content_type as pdf
        response = HttpResponse(content_type='application/pdf')

        #if download:
        #response['Content-Disposition'] = 'attachment; filename="qr-code.pdf"'

        #if display:
        response['Content-Disposition'] = 'filename="qr-code.pdf"'

        # find the template and render it.
        template = get_template(template_path)
        html = template.render(context)

        # create a pdf
        pisa_status = pisa.CreatePDF(
        html, dest=response)
        # if error then show some funny view
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response
    else:
        return redirect('https://car-plus.kyiv.ua')
    # return HttpResponse(template.render(context, request))


def page_not_found_view(request, exception):
    return render(request, 'shop/404.html', status=404)