# Generated by Django 4.1.5 on 2023-03-10 13:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('giz_app', '0013_transport_logistics_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='address',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='id_number',
        ),
    ]