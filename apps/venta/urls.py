
from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import listar_venta

urlpatterns = [
#path('listar_venta/',login_required(listar_venta.as_view()), name = 'listar_venta'),

]
