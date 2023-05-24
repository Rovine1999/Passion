# Generated by Django 4.1.5 on 2023-03-16 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('giz_app', '0023_remove_aggregator_contact_person_phone_number_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='collectioncenter',
            old_name='price',
            new_name='price_for_grade_1',
        ),
        migrations.RemoveField(
            model_name='collectioncenter',
            name='grade',
        ),
        migrations.AddField(
            model_name='collectioncenter',
            name='grade_1',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='collectioncenter',
            name='grade_2',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='collectioncenter',
            name='grade_3',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='collectioncenter',
            name='price_for_grade_2',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='collectioncenter',
            name='price_for_grade_3',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]