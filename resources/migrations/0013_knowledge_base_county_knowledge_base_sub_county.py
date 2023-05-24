# Generated by Django 4.1.5 on 2023-03-13 09:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_county_order'),
        ('resources', '0012_remove_knowledge_base_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='knowledge_base',
            name='county',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='mainapp.county'),
        ),
        migrations.AddField(
            model_name='knowledge_base',
            name='sub_county',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]