# Generated by Django 4.1.5 on 2023-03-08 19:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('mailer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='County',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_created=True, auto_now=True)),
                ('name', models.CharField(max_length=50)),
                ('county_number', models.IntegerField(blank=True, null=True)),
                ('slug', models.SlugField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='counties/preview/')),
            ],
        ),
        migrations.CreateModel(
            name='Subscriber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_created=True, auto_now=True)),
                ('first_name', models.CharField(blank=True, max_length=50, null=True)),
                ('last_name', models.CharField(blank=True, max_length=50, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True)),
                ('email', models.EmailField(max_length=254)),
                ('subscribed_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='AppConfig',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app', models.CharField(blank=True, default='main', max_length=30, null=True, unique=True)),
                ('application_url', models.CharField(blank=True, max_length=255, null=True)),
                ('listing_activated', models.BooleanField(default=True)),
                ('account_creation_activated', models.BooleanField(default=True)),
                ('account_creation_email', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='account_creation_Email', to='mailer.email')),
                ('account_creation_emailconfig', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='account_creation_email_config', to='mailer.emailconfiguration')),
                ('activate_account_email', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='account_activation_email', to='mailer.email')),
                ('activate_account_emailconfig', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='account_activation_email_config', to='mailer.emailconfiguration')),
                ('contact_email', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='contact_email', to='mailer.email')),
                ('contact_emailconfig', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='contact_emailconfig', to='mailer.emailconfiguration')),
                ('order_placement_email', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order_placement_email', to='mailer.email')),
                ('order_placement_emailconfig', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order_placement_emailconfig', to='mailer.emailconfiguration')),
                ('payment_made_email', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='payment_made_email', to='mailer.email')),
                ('payment_made_emailconfig', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='payment_made_emailconfig', to='mailer.emailconfiguration')),
                ('reset_password_email', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='password_reset_Email', to='mailer.email')),
                ('reset_password_emailconfig', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='password_reset_email_config', to='mailer.emailconfiguration')),
                ('subscription_confirmation_email', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subscription_confirmation_email', to='mailer.email')),
                ('subscription_confirmation_emailconfig', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subscription_confirmation_emailconfig', to='mailer.emailconfiguration')),
            ],
        ),
    ]