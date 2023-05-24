# Generated by Django 4.1.5 on 2023-03-08 19:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailConfiguration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('email', models.CharField(default='', max_length=100)),
                ('host', models.CharField(default='', max_length=100)),
                ('port', models.CharField(default='', max_length=100)),
                ('use_tls', models.BooleanField(default=True)),
                ('password', models.CharField(default='', max_length=100)),
                ('color', models.CharField(max_length=30)),
                ('created_on', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('body', models.TextField()),
                ('color', models.CharField(max_length=30)),
                ('identifier', models.CharField(default='', max_length=30)),
                ('created_on', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='email_created_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
