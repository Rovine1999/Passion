# Generated by Django 4.1.5 on 2023-03-10 05:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0007_remove_demofarm_description_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nursery',
            name='challenges',
        ),
    ]