# Generated by Django 4.1.5 on 2023-03-08 22:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('giz_app', '0003_alter_farmer_county'),
    ]

    operations = [
        migrations.RenameField(
            model_name='farmer',
            old_name='enumerator_number',
            new_name='enumerator_code',
        ),
    ]