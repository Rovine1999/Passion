# Generated by Django 4.1.5 on 2023-03-10 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('giz_app', '0011_remove_processors_location_remove_processors_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='coperatives',
            name='sub_county',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
