# Generated by Django 4.1.5 on 2023-03-10 08:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mainapp', '0002_county_order'),
        ('giz_app', '0007_alter_processors_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coperatives',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_created=True, auto_now=True)),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('county_number', models.IntegerField(blank=True, null=True)),
                ('email', models.EmailField(blank=True, max_length=100, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('contact_person_name', models.CharField(blank=True, max_length=200, null=True)),
                ('phone_number_contact_person', models.IntegerField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='coperatives/images/')),
                ('code', models.CharField(blank=True, max_length=20, null=True)),
                ('county', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.county')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Coperatives',
            },
        ),
    ]