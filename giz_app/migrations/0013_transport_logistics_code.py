# Generated by Django 4.1.5 on 2023-03-10 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('giz_app', '0012_coperatives_sub_county'),
    ]

    operations = [
        migrations.AddField(
            model_name='transport_logistics',
            name='code',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
