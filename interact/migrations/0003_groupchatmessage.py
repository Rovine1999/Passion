# Generated by Django 4.1.5 on 2023-03-26 22:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('resources', '0019_remove_nursery_number_of_seedlings_survived_and_more'),
        ('interact', '0002_alter_chatmessage_files'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupChatMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_created=True, auto_now=True)),
                ('text', models.TextField()),
                ('files', models.ManyToManyField(blank=True, to='interact.chatfile')),
                ('group', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='resources.farmergroup')),
                ('sender', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
