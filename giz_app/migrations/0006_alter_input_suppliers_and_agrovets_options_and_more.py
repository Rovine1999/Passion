# Generated by Django 4.1.5 on 2023-03-10 07:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('giz_app', '0005_rename_serviceprovider_processors_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='input_suppliers_and_agrovets',
            options={'verbose_name_plural': 'Input Suppliers And Agrovets'},
        ),
        migrations.AlterModelOptions(
            name='transport_logistics',
            options={'verbose_name_plural': 'Transport And Logistics'},
        ),
    ]
