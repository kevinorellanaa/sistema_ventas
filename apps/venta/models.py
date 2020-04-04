from django.db import models
from django.utils.timezone import now
from apps.inventario.models import Inventario
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
import re
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
import locale
from django.contrib import messages
from django import forms



def ValidarNIT(value):
    if re.match("^\d{4}-\d{6}-\d{3}-\d{1}$", value) == None:
        raise ValidationError(u'%s NIT Incorrecto' % value)

def ValidarDUI(value):
    if re.match("^\d{8}-\d{1}$", value) == None:
        raise ValidationError(u'%s DUI Incorrecto' % value)

def ValidarTelefono(value):
    if re.match("^\d{4}-\d{4}$", value) == None:
        raise ValidationError(u'%s Numero de Telefono Incorrecto' % value)

# Create your models here.

class Cliente(models.Model):
    nombres = models.CharField(max_length=50, null=False, blank=False)
    apellidos = models.CharField(max_length=50, null=False, blank=False)
    DUI = models.CharField(max_length=10,null=True, blank=True,help_text="formato: 00000000-0",validators=[ValidarDUI])
    NIT = models.CharField(max_length=20,null=True, blank=True,help_text="formato: 0000-000000-000-0",validators=[ValidarNIT])
    NRC = models.CharField(max_length=20,null=True, blank=True)
    telefono = models.CharField(max_length=9,null=True, blank=True,help_text="fomato: 0000-0000", validators=[ValidarTelefono])
    correo = models.EmailField(max_length=254,null=True, blank=True)
    estado = models.BooleanField(default=1)

    def __str__(self):
        return '{} {}'.format(self.nombres,self.apellidos)




class Venta(models.Model):
    fecha = models.DateField(default=now)
    hora = models.TimeField(default=now().today())
    cliente = models.ForeignKey(Cliente,on_delete=models.DO_NOTHING, null=True, blank=True)
    estado = models.BooleanField()
    total_venta = models.DecimalField(max_digits=18, decimal_places=2,null=True,blank=True,validators=[MinValueValidator(0.00)],default=0.00)

    def __str__(self):
        return '{}'.format(self.id)

# class ReporteVenta(Venta):
#     class Meta:
#         proxy = True
#         verbose_name = 'Reporte de venta'
#         verbose_name_plural = 'Reportes de Ventas'


class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta,on_delete=models.DO_NOTHING)
    articulo = models.ForeignKey(Inventario,on_delete=models.DO_NOTHING)
    cantidad = models.DecimalField(max_digits=18, decimal_places=2,validators=[MinValueValidator(0.00)])
    precio =  models.DecimalField(max_digits=18, decimal_places=2,validators=[MinValueValidator(0.00)],null=True,blank=True)
    descuento = models.DecimalField(max_digits=18, decimal_places=2,validators=[MinValueValidator(0.00)],null=True,blank=True,default=0.00)
    sub_total = models.DecimalField(max_digits=18, decimal_places=2,validators=[MinValueValidator(0.00)],null=True,blank=True,)

    #def save(self):
    #    self.precio = self.articulo.precio_venta
    #    self.sub_total = (self.precio * self.cantidad)
    #    self.sub_total = self.sub_total - ((self.descuento/100)*self.sub_total)
    #    super (DetalleVenta, self).save()


@receiver(pre_save,sender=DetalleVenta)
def DetalleVentaGuardar(sender, instance,**kwargs):
    instance.precio = instance.articulo.precio_venta
    instance.sub_total = (instance.precio * instance.cantidad)
    instance.sub_total = instance.sub_total - ((instance.descuento/100)*instance.sub_total)
    articulo_id = instance.articulo.id
    venta_id = instance.venta.id
    venta = Venta.objects.filter(pk=venta_id).first()
    if venta:
        total = instance.sub_total + venta.total_venta
        venta.total_venta = total
        venta.save()

    art = Inventario.objects.filter(pk=articulo_id).first()
    if art:
        cantidad = art.stock - instance.cantidad
        art.stock = cantidad
        art.save()

@receiver(post_delete,sender=DetalleVenta)
def DetalleVentaEliminar(sender, instance,**kwargs):

    articulo_id = instance.articulo.id
    venta_id = instance.venta.id
    venta = Venta.objects.filter(pk=venta_id).first()
    if venta:
        total = venta.total_venta - instance.sub_total
        venta.total_venta = total
        venta.save()

    art = Inventario.objects.filter(pk=articulo_id).first()
    if art:
        cantidad = art.stock + instance.cantidad
        art.stock = cantidad
        art.save()
