# Generated by Django 4.1.5 on 2023-03-08 20:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='financialprovider',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='insuranceprovider',
            name='created_by',
        ),
        migrations.DeleteModel(
            name='CountyGovernment',
        ),
        migrations.DeleteModel(
            name='FinancialProvider',
        ),
        migrations.DeleteModel(
            name='InsuranceProvider',
        ),
    ]
