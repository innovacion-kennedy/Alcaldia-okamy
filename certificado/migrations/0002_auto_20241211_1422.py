# Generated by Django 3.2.25 on 2024-12-11 14:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('certificado', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usuario',
            name='CPS',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='año_contrato',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='cedula',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='fecha_inicio',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='fecha_suscripcion',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='fecha_terminacion',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='nombre',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='objeto',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='obligaciones',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='radicado',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='role',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='sitio_expedicion',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='tiempo_ejecucion_dia',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='valor_mensual_honorarios',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='vr_inicial_contrato',
        ),
        migrations.AlterField(
            model_name='usuario',
            name='password',
            field=models.CharField(max_length=128, verbose_name='password'),
        ),
        migrations.CreateModel(
            name='Funcionario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('cedula', models.CharField(max_length=255, unique=True)),
                ('role', models.CharField(max_length=255)),
                ('CPS', models.CharField(max_length=255)),
                ('sitio_expedicion', models.CharField(max_length=255)),
                ('objeto', models.TextField()),
                ('obligaciones', models.TextField()),
                ('vr_inicial_contrato', models.IntegerField()),
                ('valor_mensual_honorarios', models.IntegerField()),
                ('fecha_suscripcion', models.DateField()),
                ('fecha_inicio', models.DateField()),
                ('fecha_terminacion', models.DateField()),
                ('tiempo_ejecucion_dia', models.IntegerField()),
                ('año_contrato', models.IntegerField()),
                ('radicado', models.CharField(max_length=255)),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='funcionario', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
