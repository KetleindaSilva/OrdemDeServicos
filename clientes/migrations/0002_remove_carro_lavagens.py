# Generated by Django 4.2.6 on 2023-11-20 00:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='carro',
            name='lavagens',
        ),
    ]