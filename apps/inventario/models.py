from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class Categoria(models.Model):
    descripcion = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        return self.descripcion

class Inventario(models.Model):
    descripcion = models.CharField(max_length=200)
    codigo_barras = models.CharField(max_length=100,null=True, blank=True)
    codigo_alternativo = models.CharField(max_length=50,null=True, blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING,null=True, blank=True)
    stock = models.DecimalField(max_digits=18, decimal_places=2,null=True, blank=True,validators=[MinValueValidator(0.00)])
    minimo = models.DecimalField(max_digits=18, decimal_places=2,null=True, blank=True,validators=[MinValueValidator(0.00)])
    precio_venta = models.DecimalField(max_digits=18, decimal_places=2,null=True, blank=True,validators=[MinValueValidator(0.00)])
    estado = models.BooleanField(default=1)

    class Meta:
        verbose_name = "Articulo"
        verbose_name_plural = "Articulos"

    def __str__(self):
        return "{} -> ({})".format(self.descripcion,self.stock)
