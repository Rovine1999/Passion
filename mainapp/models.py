from django.db import models

# Create your models here.
from mailer.models import EmailConfiguration, Email
from django.template.defaultfilters import slugify


class AppConfig(models.Model):
    app = models.CharField(max_length=30, blank=True, null=True, default="main", unique=True)

    account_creation_email = models.ForeignKey(Email, blank=True, null=True, on_delete=models.SET_NULL,
                                               related_name="account_creation_Email")

    account_creation_emailconfig = models.ForeignKey(EmailConfiguration, blank=True, null=True,
                                                     on_delete=models.SET_NULL,
                                                     related_name="account_creation_email_config")

    subscription_confirmation_email = models.ForeignKey(Email, blank=True, null=True, on_delete=models.SET_NULL,
                                                        related_name="subscription_confirmation_email")

    subscription_confirmation_emailconfig = models.ForeignKey(EmailConfiguration, blank=True, null=True,
                                                              on_delete=models.SET_NULL,
                                                              related_name="subscription_confirmation_emailconfig")

    reset_password_email = models.ForeignKey(Email, blank=True, null=True, on_delete=models.SET_NULL,
                                             related_name="password_reset_Email")
    reset_password_emailconfig = models.ForeignKey(EmailConfiguration, blank=True, null=True, on_delete=models.SET_NULL,
                                                   related_name="password_reset_email_config")

    activate_account_email = models.ForeignKey(Email, blank=True, null=True, on_delete=models.SET_NULL,
                                               related_name="account_activation_email")
    activate_account_emailconfig = models.ForeignKey(EmailConfiguration, blank=True, null=True,
                                                     on_delete=models.SET_NULL,
                                                     related_name="account_activation_email_config")

    order_placement_email = models.ForeignKey(Email, blank=True, null=True, on_delete=models.SET_NULL,
                                              related_name="order_placement_email")
    order_placement_emailconfig = models.ForeignKey(EmailConfiguration, blank=True, null=True,
                                                    on_delete=models.SET_NULL,
                                                    related_name="order_placement_emailconfig")

    payment_made_email = models.ForeignKey(Email, blank=True, null=True, on_delete=models.SET_NULL,
                                           related_name="payment_made_email")
    payment_made_emailconfig = models.ForeignKey(EmailConfiguration, blank=True, null=True,
                                                 on_delete=models.SET_NULL, related_name="payment_made_emailconfig")

    contact_email = models.ForeignKey(Email, blank=True, null=True, on_delete=models.SET_NULL,
                                      related_name="contact_email")
    contact_emailconfig = models.ForeignKey(EmailConfiguration, blank=True, null=True,
                                            on_delete=models.SET_NULL, related_name="contact_emailconfig")

    company_creation_email = models.ForeignKey(Email, blank=True, null=True, on_delete=models.SET_NULL,
                                               related_name="company_creation_email")
    company_creation_emailconfig = models.ForeignKey(EmailConfiguration, blank=True, null=True,
                                                     on_delete=models.SET_NULL,
                                                     related_name="company_creation_emailconfig")

    company_approved_email = models.ForeignKey(Email, blank=True, null=True, on_delete=models.SET_NULL,
                                               related_name="company_approved_email")
    company_approved_emailconfig = models.ForeignKey(EmailConfiguration, blank=True, null=True,
                                                     on_delete=models.SET_NULL,
                                                     related_name="company_approved_emailconfig")

    enumerator_creation_email = models.ForeignKey(Email, blank=True, null=True, on_delete=models.SET_NULL,
                                                  related_name="enumerator_creation_email")
    enumerator_creation_emailconfig = models.ForeignKey(EmailConfiguration, blank=True, null=True,
                                                        on_delete=models.SET_NULL,
                                                        related_name="enumerator_creation_emailconfig")

    enumerator_approved_email = models.ForeignKey(Email, blank=True, null=True, on_delete=models.SET_NULL,
                                                  related_name="enumerator_approved_email")
    enumerator_approved_emailconfig = models.ForeignKey(EmailConfiguration, blank=True, null=True,
                                                        on_delete=models.SET_NULL,
                                                        related_name="enumerator_approved_emailconfig")

    application_url = models.CharField(blank=True, null=True, max_length=255)
    listing_activated = models.BooleanField(default=True)
    account_creation_activated = models.BooleanField(default=True)

    def __str__(self):
        return f"Application {self.app}"


# Subscriber model
class Subscriber(models.Model):
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField()
    subscribed_date = models.DateTimeField(auto_now_add=True)

    created_on = models.DateTimeField(auto_now=True, auto_created=True)

    def __str__(self):
        return self.email


class County(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)
    county_number = models.IntegerField(blank=True, null=True)
    order = models.IntegerField(blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)
    image = models.ImageField(upload_to="counties/preview/", blank=True, null=True)

    created_on = models.DateTimeField(auto_now=True, auto_created=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super(County, self).save(*args, **kwargs)
