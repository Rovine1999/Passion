# Generated by Django 4.1.5 on 2023-03-13 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('giz_app', '0019_collectioncenter_grade_collectioncenter_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='collectioncenter',
            name='sub_county',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
