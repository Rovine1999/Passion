# Generated by Django 4.1.5 on 2023-03-13 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('giz_app', '0018_remove_profile_county_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='collectioncenter',
            name='grade',
            field=models.CharField(blank=True, choices=[('grade 1', 'Grade 1'), ('grade 2', 'Grade 2'), ('grade 3', 'Grade 3')], max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='collectioncenter',
            name='price',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
