# from django.shortcuts import render, redirect
# from reportlab.pdfgen import canvas
# from django.http import HttpResponse
# from .models import Venta
# from django.db.models import Sum
# from django.urls import reverse_lazy
from django.utils.timezone import datetime
from datetime import *
# from datetime import datetime
# from django.views.generic import ListView
# from django.http.response import responses


# Create your views here.
# def hola_pdf(request):
#     # Crea un objeto HttpResponse  con las cabeceras PDF correctas.
#
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename=hello.pdf'
#
#     # Crea un objeto PDF, usando el objeto como un "archivo".
#     p = canvas.Canvas(response)
#     resultado = Venta.objects.filter(fecha='2020-03-03').aggregate(Sum('total_venta'))
#
#     #Inventario.objects.all()
#     # Dibuja cosas en el PDF. Aqui se genera el PDF.
#     # Consulta la documentación de ReportLab para una lista completa de funcionalidades.
#     p.drawString(50, 800, str(resultado))
#
#
#     # Cierra el objeto PDF limpiamente y termina.
#     p.showPage()
#     p.save()
#     redirect('admin:index')
#     return response
#
# #class VentaList(ListView):
# #    model = Venta
# #    template_name = 'admin/VentaListView.html'
#
# #class ListarVenta(ListView):
# #    model = Venta
# #    template_name = 'admin/reporteventas.html'
# #    queryset = Venta.objects.all()
#
#
# def venta_list(request):
#     ventas = Venta.objects.all()
#     return HttpResponse('admin/reporteventas.html', {'ventas': ventas})

from django.shortcuts import render,redirect
from django.views.generic import TemplateView, ListView
from .models import Venta
# Create your views here



class listar_venta(ListView):
    model = Venta
    queryset = Venta.objects.filter(fecha = datetime.now())
    template_name = 'venta/reporteventas.html'
