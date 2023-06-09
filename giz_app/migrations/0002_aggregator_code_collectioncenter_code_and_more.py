# Generated by Django 4.1.5 on 2023-03-08 20:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mainapp', '0001_initial'),
        ('giz_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='aggregator',
            name='code',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='collectioncenter',
            name='code',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='serviceprovider',
            name='code',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.CreateModel(
            name='InsuranceProvider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_on', models.DateTimeField(auto_created=True, auto_now=True)),
                ('created_on', models.DateTimeField(auto_created=True, auto_now_add=True)),
                ('code', models.CharField(blank=True, max_length=20, null=True)),
                ('county_number', models.IntegerField(blank=True, null=True)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('location', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='stakeholders/insuranceproviders/')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Insurance Providers',
            },
        ),
        migrations.CreateModel(
            name='FinancialProvider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_on', models.DateTimeField(auto_created=True, auto_now=True)),
                ('created_on', models.DateTimeField(auto_created=True, auto_now_add=True)),
                ('code', models.CharField(blank=True, max_length=20, null=True)),
                ('county_number', models.IntegerField(blank=True, null=True)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('image', models.ImageField(upload_to='stakeholders/financialproviders/')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Financial Providers',
            },
        ),
        migrations.CreateModel(
            name='Enumerator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_created=True, auto_now=True)),
                ('code', models.CharField(blank=True, max_length=20, null=True)),
                ('county_number', models.IntegerField()),
                ('county', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET, to='mainapp.county')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CountyGovernment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_on', models.DateTimeField(auto_created=True, auto_now=True)),
                ('created_on', models.DateTimeField(auto_created=True, auto_now_add=True)),
                ('code', models.CharField(blank=True, max_length=20, null=True)),
                ('county_number', models.IntegerField(blank=True, null=True)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('location', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='stakeholders/countygovt/')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'County Governments',
            },
        ),
        migrations.AddField(
            model_name='farmer',
            name='enumerator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='giz_app.enumerator'),
        ),
    ]
