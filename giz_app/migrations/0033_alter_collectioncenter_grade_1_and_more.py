# Generated by Django 4.1.5 on 2023-03-20 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('giz_app', '0032_collectioncenter_flashsale'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collectioncenter',
            name='grade_1',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='collectioncenter',
            name='grade_2',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='collectioncenter',
            name='grade_3',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
