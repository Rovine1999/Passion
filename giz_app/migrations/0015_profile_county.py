# Generated by Django 4.1.5 on 2023-03-10 13:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_county_order'),
        ('giz_app', '0014_remove_profile_address_remove_profile_id_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='county',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.county'),
        ),
    ]
