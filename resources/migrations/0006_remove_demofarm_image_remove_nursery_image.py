# Generated by Django 4.1.5 on 2023-03-09 06:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0005_remove_demofarm_challenges'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='demofarm',
            name='image',
        ),
        migrations.RemoveField(
            model_name='nursery',
            name='image',
        ),
    ]