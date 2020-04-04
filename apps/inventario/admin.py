from django.contrib import admin
from .models import Categoria,Inventario
from import_export import resources
from import_export.admin import ImportExportModelAdmin


class InventarioResource(resources.ModelResource):
    class Meta:
        model = Inventario


class InventarioAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ('descripcion','codigo_barras','codigo_alternativo','categoria','stock','minimo','precio_venta','estado')
    list_filter_links = ('categoria')
    search_fields = ('descripcion','codigo_barras')
    autocomplete_fields_links = ('categoria')
    resource_class = InventarioResource




admin.site.register(Categoria)
admin.site.register(Inventario,InventarioAdmin)
