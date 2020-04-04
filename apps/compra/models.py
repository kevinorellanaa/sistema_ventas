from django.db import models
from django.utils.timezone import now
from apps.inventario.models import Inventario
from django.core.exceptions import ValidationError
import re, operator
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver


def ValidarNIT(value):
    if re.match("^\d{4}-\d{6}-\d{3}-\d{1}$", value) == None:
        raise ValidationError(u'%s NIT Incorrecto' % value)

def ValidarDUI(value):
    if re.match("^\d{8}-\d{1}$", value) == None:
        raise ValidationError(u'%s DUI Incorrecto' % value)

def ValidarTelefono(value):
    if re.match("^\d{4}-\d{4}$", value) == None:
        raise ValidationError(u'%s Numero de Telefono Incorrecto' % value)


class Proveedor(models.Model):
    nombre = models.CharField(max_length=200, null=False, blank=False)
    DUI = models.CharField(max_length=10,null=True, blank=True,help_text="formato: 00000000-0",validators=[ValidarDUI])
    NIT = models.CharField(max_length=20,null=True, blank=True,help_text="formato: 0000-000000-000-0",validators=[ValidarNIT])
    NRC = models.CharField(max_length=20,null=True, blank=True)
    telefono = models.CharField(max_length=9,null=True, blank=True,help_text="fomato: 0000-0000", validators=[ValidarTelefono])
    correo = models.EmailField(max_length=254,null=True, blank=True)


    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"


class Compra(models.Model):
    factura = models.CharField(max_length=50,null=True,blank=True)
    fecha = models.DateTimeField(default=now)
    proveedor = models.ForeignKey(Proveedor,on_delete=models.DO_NOTHING)
    total_compra = models.DecimalField(max_digits=18, decimal_places=2,null=True,blank=True,validators=[MinValueValidator(0.00)],default=0.00)

    def __str__(self):
        return self.factura

class DetalleCompra(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.DO_NOTHING)
    articulo = models.ForeignKey(Inventario,on_delete=models.DO_NOTHING)
    precio = models.DecimalField(max_digits=18, decimal_places=2)
    cantidad = models.DecimalField(max_digits=18, decimal_places=2,)
    sub_total = models.DecimalField(max_digits=18, decimal_places=2,null=True,blank=True,)

    def __str__(self):
        return self.articulo.descripcion

    def save(self):
        self.sub_total = self.precio * self.cantidad
        super (DetalleCompra, self).save()


@receiver(pre_save,sender=DetalleCompra)
def DetalleCompraGuardar(sender, instance,**kwargs):

    articulo_id = instance.articulo.id
    compra_id = instance.compra.id
    compra = Compra.objects.filter(pk=compra_id).first()
    if compra:
        total = instance.sub_total + compra.total_compra
        compra.total_compra = total
        compra.save()

    art = Inventario.objects.filter(pk=articulo_id).first()
    if art:
        cantidad = art.stock + instance.cantidad
        art.stock = cantidad
        art.save()

@receiver(post_delete,sender=DetalleCompra)
def DetalleCompraEliminar(sender, instance,**kwargs):

    articulo_id = instance.articulo.id
    compra_id = instance.compra.id
    compra = Compra.objects.filter(pk=compra_id).first()
    if compra:
        total = compra.total_compra - instance.sub_total
        compra.total_compra = total
        compra.save()

    art = Inventario.objects.filter(pk=articulo_id).first()
    if art:
        cantidad = art.stock - instance.cantidad
        art.stock = cantidad
        art.save()
