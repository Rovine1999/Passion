# Generated by Django 4.1.5 on 2023-03-15 13:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0016_rename_no_of_farmers_served_nursery_no_of_farmers_availaible'),
    ]

    operations = [
        migrations.RenameField(
            model_name='nursery',
            old_name='no_of_farmers_availaible',
            new_name='no_of_seedlings_availaible',
        ),
    ]
