# Generated by Django 4.1.5 on 2023-03-08 19:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('resources', '0001_initial'),
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_created=True, auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=100)),
                ('subject', models.CharField(max_length=100)),
                ('message', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='ServiceProvider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_created=True, auto_now=True)),
                ('location', models.CharField(blank=True, default='', max_length=20, null=True)),
                ('company_name', models.CharField(default='', max_length=200)),
                ('county_number', models.IntegerField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='service-providers/images/')),
                ('description', models.TextField(blank=True, null=True)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_created=True, auto_now=True)),
                ('address', models.CharField(blank=True, max_length=150, null=True)),
                ('county_number', models.IntegerField(blank=True, null=True)),
                ('id_number', models.CharField(blank=True, max_length=50, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=16, null=True)),
                ('alt_phone_number', models.CharField(blank=True, max_length=16, null=True)),
                ('profile_photo', models.ImageField(blank=True, null=True, upload_to='profile_photo')),
                ('year_of_birth', models.IntegerField(blank=True, null=True)),
                ('gender', models.CharField(blank=True, choices=[('male', 'Male'), ('female', 'Female')], max_length=20, null=True)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Offtaker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_created=True, auto_now=True)),
                ('location', models.CharField(max_length=20)),
                ('county_number', models.IntegerField(blank=True, null=True)),
                ('name', models.TextField(blank=True, null=True)),
                ('vehicle_number', models.CharField(default='', max_length=20)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Farmer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_created=True, auto_now=True)),
                ('county_number', models.IntegerField(blank=True, null=True)),
                ('county', models.CharField(blank=True, max_length=20, null=True)),
                ('sub_county', models.CharField(blank=True, max_length=20, null=True)),
                ('postal_address', models.TextField(blank=True, null=True)),
                ('acreage', models.CharField(blank=True, max_length=20, null=True)),
                ('enumerator_number', models.CharField(blank=True, max_length=20, null=True)),
                ('landmark', models.TextField(blank=True, null=True)),
                ('selling_place', models.CharField(blank=True, max_length=255, null=True)),
                ('farmer_group_code', models.CharField(blank=True, max_length=30, null=True)),
                ('farmer_number', models.CharField(blank=True, max_length=20, null=True)),
                ('farmer_group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='resources.farmergroup')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CollectionCenter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_created=True, auto_now=True)),
                ('county_number', models.IntegerField(blank=True, null=True)),
                ('name', models.CharField(max_length=512)),
                ('slug', models.SlugField(blank=True, null=True)),
                ('lat', models.CharField(max_length=512)),
                ('lon', models.CharField(max_length=512)),
                ('description', models.TextField()),
                ('county', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='mainapp.county')),
            ],
        ),
        migrations.CreateModel(
            name='Aggregator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_created=True, auto_now=True)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('county_number', models.IntegerField(blank=True, null=True)),
                ('mobile_number', models.CharField(blank=True, max_length=30, null=True)),
                ('location', models.CharField(blank=True, max_length=100, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
