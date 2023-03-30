import requests
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.template import loader
import datetime
from django.views.generic.list import ListView
from .models import Tire, QuickOrderNewTire
from .forms import QuickOrderNewTireForm
from .filters import TireFilter

# Create your views here.

# class Home(ListView):
    
#     queryset = Tire.objects.all().order_by('-in_stock')
#     paginate_by = 2

#     template_name = 'new_tire/new-tire-list.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['filter'] = TireFilter(self.request.GET, queryset=self.get_queryset())

        
#         return context

def Home(request):
    f = TireFilter(request.GET, queryset=Tire.objects.all().order_by('-in_stock'))

    paginator = Paginator(f.qs, 33)
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)

    context = {
        'filter': f,
        'paginator_filter': paged_listings
    }

    if request.method == 'GET':
        print('Get')
        return render(request, 'new_tire/new-tire-list.html', context)


def TireDetail(request, slug):

    template = loader.get_template('new_tire/new_tire_detail.html')
    tire = get_object_or_404(Tire, slug=slug)

    
    if request.method == 'POST':
        form = QuickOrderNewTireForm(request.POST)
        
        #form.fields['phone'].validators = [MinValueValidator(500000000, message='Не вистачає цифри. Приклад: 0971234455'),
        #                                   MaxValueValidator(999999999, message='Ви вели забагато цифр. Приклад: 0971234455')]

        if form.is_valid():
            qo = form.save(commit=False)
            try:
                QuickOrderNewTire.objects.get(phone=qo.phone, tire=tire)
                messages.success(request, "Ваше замовлення отримано менеджером. Чекайте на дзвінок.")
            except QuickOrderNewTire.DoesNotExist:
                if request.user.username == 'AnonymouseUser':
                        
                    obj, create = QuickOrderNewTire.objects.update_or_create(phone=qo.phone, tire=tire, price=tire.price_two)
                    messages.success(request, "Дякуємо! Заявка надіслана успішно! Скоро з Вами зв'яжеться наш менеджер.")
                else:
                    
                    obj, create = QuickOrderNewTire.objects.update_or_create(phone=qo.phone, tire=tire, price=tire.price_two)
                    messages.success(request, "Дякуємо! Заявка надіслана успішно! Скоро з Вами зв'яжеться наш менеджер.")
    else:
        form = QuickOrderNewTireForm()
    

    context = {
        'tire': tire,
        'form': form,
    }

    return HttpResponse(template.render(context, request))



def OlderRecords(request):

    template = loader.get_template('tires/old_tire.html')
    
    today = datetime.datetime.now() - datetime.timedelta(days=1)
    old_records = Tire.objects.filter(updated__lt=today, in_stock__gt=0 )
    counter = old_records.count()

    context = {
        'old_records': old_records,
        'counter': counter,
    }

    return HttpResponse(template.render(context, request))


def UpdatePrice(request):
    if request.user.is_superuser:
        today = datetime.datetime.now() - datetime.timedelta(hours=15)
        old_records = Tire.objects.filter(updated__lt=today, in_stock__gt=0 ).update(in_stock=0)
    else:
        pass

    return redirect('/')

