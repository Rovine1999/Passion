# Generated by Django 4.1.5 on 2023-03-09 01:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0003_extensionservice'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='extensionservice',
            options={'verbose_name_plural': 'Extension Services'},
        ),
        migrations.AlterField(
            model_name='extensionservice',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
