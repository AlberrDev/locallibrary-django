# Generated by Django 4.2.7 on 2024-02-17 12:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('catalog', '0007_alter_bookinstance_options_alter_book_ficheros_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Perfiles',
            fields=[
                ('dni', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('direccion', models.CharField(max_length=50)),
                ('provincia', models.CharField(max_length=40)),
                ('telefono', models.CharField(max_length=40)),
            ],
            options={
                'permissions': (('mandar_mensajes', 'Mandar mensajes'), ('recibir_mensajes', 'Recibir Mensajes')),
            },
        ),
        migrations.AlterModelOptions(
            name='bookinstance',
            options={'ordering': ['due_back'], 'permissions': (('can_mark_returned', 'Set book as returned'), ('can_generate_pdf', 'Generate PDF'), ('permiso1', 'Crear Usuario'), ('permiso2', 'Crear Perfil Usuario'))},
        ),
    ]
