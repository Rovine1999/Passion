# Generated by Django 4.1.5 on 2023-03-10 08:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('giz_app', '0008_coperatives'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='farmer',
            name='postal_address',
        ),
        migrations.AddField(
            model_name='farmer',
            name='coperatives',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='giz_app.coperatives'),
        ),
    ]
