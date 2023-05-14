from django.shortcuts import render
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic.detail import DetailView
from .models import StorageInfo, Client

# Create your views here.

class ClientDetail(DetailView):
    model = Client
    template_name = 'storage_info/client_info.html'


class StorageInfoDetail(DetailView):
    model = StorageInfo
    template_name = 'storage_info/storage_info.html'

def render_pdf_storage_info(request, id):
    if request.user.is_authenticated:
        storage_info = get_object_or_404(StorageInfo, id=id)

        template_path = 'storage_info/storage_detail_pdf.html'


        context = {'storage_info': storage_info}
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