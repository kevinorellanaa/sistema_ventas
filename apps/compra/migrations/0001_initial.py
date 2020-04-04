# Generated by Django 3.0.3 on 2020-03-30 04:42

import apps.compra.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('inventario', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Compra',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('factura', models.CharField(blank=True, max_length=50, null=True)),
                ('fecha', models.DateTimeField(default=django.utils.timezone.now)),
                ('total_compra', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=18, null=True, validators=[django.core.validators.MinValueValidator(0.0)])),
            ],
        ),
        migrations.CreateModel(
            name='Proveedor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('DUI', models.CharField(blank=True, help_text='formato: 00000000-0', max_length=10, null=True, validators=[apps.compra.models.ValidarDUI])),
                ('NIT', models.CharField(blank=True, help_text='formato: 0000-000000-000-0', max_length=20, null=True, validators=[apps.compra.models.ValidarNIT])),
                ('NRC', models.CharField(blank=True, max_length=20, null=True)),
                ('telefono', models.CharField(blank=True, help_text='fomato: 0000-0000', max_length=9, null=True, validators=[apps.compra.models.ValidarTelefono])),
                ('correo', models.EmailField(blank=True, max_length=254, null=True)),
            ],
            options={
                'verbose_name': 'Proveedor',
                'verbose_name_plural': 'Proveedores',
            },
        ),
        migrations.CreateModel(
            name='DetalleCompra',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('precio', models.DecimalField(decimal_places=2, max_digits=18)),
                ('cantidad', models.DecimalField(decimal_places=2, max_digits=18)),
                ('sub_total', models.DecimalField(blank=True, decimal_places=2, max_digits=18, null=True)),
                ('articulo', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='inventario.Inventario')),
                ('compra', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='compra.Compra')),
            ],
        ),
        migrations.AddField(
            model_name='compra',
            name='proveedor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='compra.Proveedor'),
        ),
    ]
