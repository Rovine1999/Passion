# Generated by Django 4.1.5 on 2023-04-17 17:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0003_appconfig_company_approved_email_and_more'),
        ('resources', '0019_remove_nursery_number_of_seedlings_survived_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='farmergroup',
            name='county',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='farmer_groups', to='mainapp.county'),
        ),
    ]
