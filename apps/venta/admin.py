from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import Cliente,Venta,DetalleVenta,Inventario
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.db.models import Sum
from django.urls import path
from django.utils import timezone
from datetime import datetime
from django.utils.timezone import now



# Register your models here.
class VentaResource(resources.ModelResource):
    class Meta:
        model = Venta

class DetalleVentaInline(admin.TabularInline):
    model = DetalleVenta
    fields = ('articulo','cantidad','descuento','precio','sub_total')
    extra = 1
    readonly_fields =('sub_total','precio')
    autocomplete_fields = ('articulo',)


class VentaAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    inlines = [DetalleVentaInline,]
    list_display = ('id','fecha','hora','cliente','estado','total_venta')
    fields = (('fecha','hora', 'cliente'),'estado', 'total_venta')
    readonly_fields = ('total_venta',)
    list_filter = ('fecha','cliente',)
    search_fields = ('id','cliente__nombres','cliente__apellidos')
    date_hierarchy = 'fecha'
    resource_class = VentaResource
    def changelist_view(self, request, extra_context=None):

        #semana = timezone.now() - timedelta(days=7)
        #totalsemana = Venta.objects.filter(fecha__range=[semana,timezone.now()]).aggregate(totalsemana=Sum('total_venta'))['totalsemana']
        totaldia = Venta.objects.filter(fecha=timezone.now(), estado="True").aggregate(totaldia=Sum('total_venta'))['totaldia']
        context = {
            'totaldia': totaldia,
            #'totalsemana':totalsemana,
        }
        return super(VentaAdmin, self).changelist_view(request, extra_context=context)


class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombres', 'apellidos', 'DUI','NIT','NRC','telefono','correo','estado')
    search_fields = ('nombres','apellidos')

# @admin.register(ReporteVenta)
# class ReporteVentaAdmin(ModelAdmin):
#     change_list_template = 'admin/reporteventas.html'
#     exclude = ('id','fecha', 'cliente','estado','total_venta')
#     def has_add_permission(self, request):
#         return False
#     def has_change_permission(self, request):
#         return False




admin.site.register(Cliente,ClienteAdmin)
admin.site.register(Venta,VentaAdmin)
