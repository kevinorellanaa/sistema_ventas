from django.contrib import admin
from .models import Proveedor,Compra,DetalleCompra
from django import forms
from django.db.models import Sum

# Register your models here.

class DetalleCompraForm(forms.ModelForm):
    class Meta:
        model = DetalleCompra
        fields = ['compra','articulo','cantidad','precio','sub_total']
        readonly_fields =('sub_total',)


#class DetalleCompraAdmin(admin.ModelAdmin):
#    model = DetalleCompra



class DetalleCompraInline(admin.TabularInline,):
    model = DetalleCompra
    extra = 1
    fields = ['compra','articulo','cantidad','precio','sub_total']
    readonly_fields = ('sub_total',)
    autocomplete_fields = ('articulo',)


class CompraAdmin(admin.ModelAdmin):
    inlines = [DetalleCompraInline,]
    list_display = ('factura', 'fecha', 'proveedor','total_compra',)
    fields = (('factura', 'fecha'), 'proveedor', 'total_compra')
    readonly_fields =('total_compra',)
    search_fields = ('factura','fecha')
    date_hierarchy = 'fecha'
    list_filter = ('fecha','proveedor',)



class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('nombre','DUI','NIT','NRC','telefono','correo',)
    search_fields = ('nombre','DUI','NIT','NRC')

admin.site.register(Proveedor,ProveedorAdmin)
admin.site.register(Compra,CompraAdmin)
#admin.site.register(DetalleCompra,DetalleCompraAdmin)
