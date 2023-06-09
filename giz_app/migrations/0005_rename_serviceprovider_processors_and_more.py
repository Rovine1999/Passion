# Generated by Django 4.1.5 on 2023-03-10 07:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mainapp', '0002_county_order'),
        ('giz_app', '0004_rename_enumerator_number_farmer_enumerator_code'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ServiceProvider',
            new_name='Processors',
        ),
        migrations.CreateModel(
            name='Transport_logistics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_created=True, auto_now=True)),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('county_number', models.IntegerField(blank=True, null=True)),
                ('sub_county', models.CharField(blank=True, default='', max_length=20, null=True)),
                ('location', models.CharField(blank=True, default='', max_length=20, null=True)),
                ('email', models.EmailField(blank=True, max_length=100, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('contact_person_name', models.CharField(blank=True, max_length=200, null=True)),
                ('phone_number_contact_person', models.IntegerField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='transport-logistics/images/')),
                ('county', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.county')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Input_suppliers_and_agrovets',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_created=True, auto_now=True)),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('county_number', models.IntegerField(blank=True, null=True)),
                ('sub_county', models.CharField(blank=True, default='', max_length=20, null=True)),
                ('location', models.CharField(blank=True, default='', max_length=20, null=True)),
                ('email', models.EmailField(blank=True, max_length=100, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('contact_person_name', models.CharField(blank=True, max_length=200, null=True)),
                ('phone_number_contact_person', models.IntegerField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='input-suppliers/images/')),
                ('code', models.CharField(blank=True, max_length=20, null=True)),
                ('county', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.county')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
