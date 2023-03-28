from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.template import loader
import datetime
from django.views.generic.list import ListView
from .models import Tire
from .filters import TireFilter

# Create your views here.

class Home(ListView):
    
    queryset = Tire.objects.all()
    template_name = 'new_tire/new-tire-list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = TireFilter(self.request.GET, queryset=self.get_queryset())
        return context
    

def TireDetail(request, slug):

    template = loader.get_template('new_tire/new_tire_detail.html')
    tire = get_object_or_404(Tire, slug=slug)
    

    context = {
        'tire': tire,
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


def OlderRecordsUpdate(request):

    today = datetime.datetime.now() - datetime.timedelta(days=1)
    old_records = Tire.objects.filter(updated__lt=today, in_stock__gt=0 ).update(in_stock=0)

    return redirect('/')

