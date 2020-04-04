"""sistema_ventas URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:

Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from apps.inventario.views import base_site
from django.views.generic import TemplateView
from apps.venta.views import listar_venta
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from apps.venta.models import Venta


admin.site.site_header = 'Knows Software'
admin.site.site_title = 'Tablero Administrativo'
admin.site.index_title = 'Bienvenido al sitio Administrativo'


urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin/', TemplateView.as_view(template_name='admin/base_site.html')),
    # path('ventas/', views.venta_list, name='venta_list'),
    # path('listar_venta/',ListarVenta.as_view(), name = 'listar_venta'),
    #path('venta/',include(('apps.venta.urls','Venta'))),
    path('listar_venta/',listar_venta.as_view(template_name='admin/reporteventas.html')),


    #path('admin/reportes', TemplateView.as_view(template_name='reportes.html')),

]
