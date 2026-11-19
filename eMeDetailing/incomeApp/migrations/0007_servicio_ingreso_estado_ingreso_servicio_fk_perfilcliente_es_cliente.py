import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('incomeApp', '0006_ingreso_cliente_perfilcliente'),
    ]

    operations = [
        migrations.CreateModel(
            name='Servicio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50, unique=True, verbose_name='Nombre del servicio')),
                ('descripcion', models.TextField(blank=True, verbose_name='Descripción')),
                ('precio_citycar', models.IntegerField(default=13000, verbose_name='Precio Citycar')),
                ('precio_sedan', models.IntegerField(default=16000, verbose_name='Precio Sedan')),
                ('precio_suv', models.IntegerField(default=19000, verbose_name='Precio SUV')),
            ],
            options={
                'verbose_name': 'Servicio',
                'verbose_name_plural': 'Servicios',
            },
        ),
        migrations.AddField(
            model_name='perfilcliente',
            name='es_cliente',
            field=models.BooleanField(default=True, verbose_name='Es Cliente'),
        ),
        migrations.AddField(
            model_name='ingreso',
            name='estado',
            field=models.CharField(
                choices=[
                    ('Pendiente', 'Pendiente'),
                    ('Confirmada', 'Confirmada'),
                    ('Realizada', 'Realizada'),
                    ('Cancelada', 'Cancelada'),
                ],
                default='Pendiente',
                max_length=20,
                verbose_name='Estado de la reserva'
            ),
        ),
        migrations.AddField(
            model_name='ingreso',
            name='servicio_fk',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='reservas',
                to='incomeApp.servicio',
                verbose_name='Servicio'
            ),
        ),
        migrations.AlterField(
            model_name='ingreso',
            name='servicio',
            field=models.CharField(max_length=50),
        ),
    ]
