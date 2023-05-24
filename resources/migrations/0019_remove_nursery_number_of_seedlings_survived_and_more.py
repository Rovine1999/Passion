# Generated by Django 4.1.5 on 2023-03-15 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0018_rename_no_of_seedlings_availaible_nursery_number_of_seedlings_availaible'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nursery',
            name='number_of_seedlings_survived',
        ),
        migrations.AlterField(
            model_name='nursery',
            name='number_of_seedlings_availaible',
            field=models.IntegerField(blank=True, help_text='This is for nurseries', null=True),
        ),
    ]
