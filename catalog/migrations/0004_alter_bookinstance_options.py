# Generated by Django 4.2.7 on 2024-01-24 11:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_bookinstance_borrower'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bookinstance',
            options={'ordering': ['due_back'], 'permissions': (('can_mark_returned', 'Set book as returned'), ('can_generate_pdf', 'Generate PDF'))},
        ),
    ]
