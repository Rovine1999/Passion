from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from mainapp.models import County
from resources.models import FarmerGroup
from django.conf import settings

from mailer.views import send_account_creation_email
from mailer.utils import send_custom_email

import random
import string


def generate_uuid():
    """
    Generate a random UUID consisting of 5 uppercase letters and numbers.
    """
    characters = string.ascii_uppercase + string.digits
    uuid = ''.join(random.choice(characters) for _ in range(5))
    return uuid


GENDER_CHOICES = (
    ('male', 'Male'),
    ('female', 'Female'),
)

GRADE_CHOICES = (
    ("grade 1", "Grade 1"),
    ("grade 2", "Grade 2"),
    ("grade 3", "Grade 3")
)


@receiver(post_save, sender=User)
def send_new_account_creation_email(sender, instance, created, **kwargs):
    """
    This signal listens for user creation and fires sending an account creation email
    """
    if created:
        # send_account_creation_email(instance)
        return True


class Profile(models.Model):
    user = models.OneToOneField(
        User, blank=True, null=True, on_delete=models.CASCADE)
    county = models.ForeignKey(
        County, blank=True, null=True, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=16, blank=True, null=True)
    alt_phone_number = models.CharField(max_length=16, blank=True, null=True)
    profile_photo = models.ImageField(
        upload_to='profile_photo', blank=True, null=True)
    year_of_birth = models.IntegerField(blank=True, null=True)
    gender = models.CharField(choices=GENDER_CHOICES,
                              blank=True, null=True, max_length=20)
    friends = models.ManyToManyField(User, related_name='friends', blank=True)

    created_on = models.DateTimeField(auto_now=True, auto_created=True)

    def __str__(self):
        return self.user.username


class Farmer(models.Model):
    user = models.OneToOneField(
        User, blank=True, null=True, on_delete=models.CASCADE)
    county = models.ForeignKey(
        'mainapp.County', on_delete=models.SET_NULL, blank=True, null=True)
    county_name = models.CharField(max_length=20, blank=True, null=True)
    county_number = models.IntegerField(blank=True, null=True, default=0)

    sub_county = models.CharField(max_length=20, blank=True, null=True)
    # postal_address = models.TextField(blank=True, null=True)
    acreage = models.CharField(max_length=20, blank=True, null=True)

    enumerator = models.ForeignKey(
        'Enumerator', blank=True, null=True, on_delete=models.SET_NULL)
    enumerator_code = models.CharField(max_length=20, blank=True, null=True)

    landmark = models.TextField(blank=True, null=True)

    selling_place = models.CharField(max_length=255, blank=True, null=True)

    farmer_group = models.ForeignKey(
        'resources.FarmerGroup', blank=True, null=True, on_delete=models.SET_NULL)
    farmer_group_code = models.CharField(max_length=30, blank=True, null=True)

    coperatives = models.ForeignKey(
        'Coperatives', blank=True, null=True, on_delete=models.CASCADE)

    # offtaker = models.ForeignKey(Offtaker, blank=True, null=True, on_delete=models.CASCADE)

    farmer_number = models.CharField(max_length=20, blank=True, null=True)

    created_on = models.DateTimeField(auto_now=True, auto_created=True)

    def __str__(self):
        return self.user.first_name

    def save(self, *args, **kwargs):
        if not self.pk:
            farmer_group = FarmerGroup.objects.filter(
                code=self.farmer_group_code).first()
            self.farmer_group = farmer_group if self.farmer_group is None else self.farmer_group
            enumerator = Enumerator.objects.filter(
                code=self.enumerator_code).first()
            self.enumerator = enumerator if self.enumerator is None else self.enumerator
            county = County.objects.filter(
                county_number=self.county_number).first()
            self.county = county if self.county is None else self.county

        return super().save(*args, **kwargs)


class Offtaker(models.Model):
    user = models.OneToOneField(
        User, blank=True, null=True, on_delete=models.SET_NULL)
    location = models.CharField(max_length=20)
    county_number = models.IntegerField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    vehicle_number = models.CharField(max_length=20, default="")
    phone_number = models.IntegerField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now=True, auto_created=True)


class Company(models.Model):
    user = models.OneToOneField(User, blank=True, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=255, blank=False, null=False)
    code = models.CharField(max_length=20, blank=False, null=True)  # E4I-[REST]

    approved = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now=True, auto_created=True)

    def __str__(self):
        return self.name


@receiver(post_save, sender=Company)
def send_company_creation_email(sender, instance, created, **kwargs):
    """
    This signal listens for company creation and fires sending a company creation email
    """
    if created:
        send_custom_email('company_creation', instance, settings.ADMIN_EMAILS)
        return True


class Enumerator(models.Model):
    user = models.OneToOneField(
        User, blank=True, null=True, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, blank=False, null=True, on_delete=models.SET_NULL)
    code = models.CharField(max_length=20, blank=True, null=True)
    county = models.ForeignKey(
        'mainapp.County', blank=True, null=True, on_delete=models.SET)
    county_number = models.IntegerField(blank=True, null=True, default=0)
    phone_number = models.IntegerField(blank=True, null=True)

    approved = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now=True, auto_created=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    def save(self, *args, **kwargs):
        if not self.pk:
            county = County.objects.filter(
                county_number=self.county_number).first()
            self.county = county if self.county is None else self.county
            # Generate a new UUID for a new instance of the model
            while True:
                uuid = self.company.code + generate_uuid()
                if not Enumerator.objects.filter(code=uuid).exists():
                    self.code = uuid
                    break

        return super().save(*args, **kwargs)


@receiver(post_save, sender=Enumerator)
def send_enumerator_creation_email(sender, instance, created, **kwargs):
    """
    This signal listens for enumerator creation and fires sending a company creation email
    """
    if created:
        send_custom_email('enumerator_creation', instance, settings.ADMIN_EMAILS)
        return True


class AbstractServiceProvider(models.Model):
    user = models.OneToOneField(
        User, blank=True, null=True, on_delete=models.CASCADE, default=None)
    company_name = models.CharField(
        max_length=200, blank=False, null=False, default="")
    code = models.CharField(max_length=20, blank=True, null=True)
    county = models.ForeignKey(County,
                               blank=True, null=True, on_delete=models.SET_NULL, default=None)
    sub_county = models.CharField(max_length=200, blank=True, null=True)
    county_number = models.IntegerField(blank=True, null=True)
    image = models.ImageField(
        upload_to='processors/images/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    # contact_person_name = models.CharField(max_length=200, blank=True, null=True)
    # contact_person_phone_number = models.IntegerField(blank=True, null=True)

    created_on = models.DateTimeField(auto_now=True, auto_created=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.company_name


class Coperatives(AbstractServiceProvider):
    class Meta:
        verbose_name_plural = 'Coperatives'

    def save(self, *args, **kwargs):
        if not self.pk:
            # Generate a new UUID for a new instance of the model
            while True:
                uuid = generate_uuid()
                if not Coperatives.objects.filter(code=uuid).exists():
                    self.code = uuid
                    break

        return super().save(*args, **kwargs)


class Processors(AbstractServiceProvider):
    class Meta:
        verbose_name_plural = "Processors"

    def save(self, *args, **kwargs):
        if not self.pk:
            # Generate a new UUID for a new instance of the model
            while True:
                uuid = generate_uuid()
                if not Processors.objects.filter(code=uuid).exists():
                    self.code = uuid
                    break

        return super().save(*args, **kwargs)


class TransportLogistics(AbstractServiceProvider):
    class Meta:
        verbose_name_plural = "Transport And Logistics"

    def save(self, *args, **kwargs):
        if not self.pk:
            # Generate a new UUID for a new instance of the model
            while True:
                uuid = generate_uuid()
                if not TransportLogistics.objects.filter(code=uuid).exists():
                    self.code = uuid
                    break

        return super().save(*args, **kwargs)


class InputSuppliersAndAgrovets(AbstractServiceProvider):
    class Meta:
        verbose_name_plural = 'Input Suppliers And Agrovets'

    def save(self, *args, **kwargs):
        if not self.pk:
            # Generate a new UUID for a new instance of the model
            while True:
                uuid = generate_uuid()
                if not InputSuppliersAndAgrovets.objects.filter(code=uuid).exists():
                    self.code = uuid
                    break

        return super().save(*args, **kwargs)


class FinancialProvider(AbstractServiceProvider):
    class Meta:
        verbose_name_plural = 'Financial Providers'

    def save(self, *args, **kwargs):
        if not self.pk:
            # Generate a new UUID for a new instance of the model
            while True:
                uuid = generate_uuid()
                if not FinancialProvider.objects.filter(code=uuid).exists():
                    self.code = uuid
                    break

        return super().save(*args, **kwargs)


class InsuranceProvider(AbstractServiceProvider):
    class Meta:
        verbose_name_plural = 'Insurance Providers'

    def save(self, *args, **kwargs):
        if not self.pk:
            # Generate a new UUID for a new instance of the model
            while True:
                uuid = generate_uuid()
                if not InsuranceProvider.objects.filter(code=uuid).exists():
                    self.code = uuid
                    break

        return super().save(*args, **kwargs)


class CountyGovernment(AbstractServiceProvider):
    website = models.URLField(max_length=512, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'County Governments'

    def __str__(self) -> str:
        return self.company_name

    def save(self, *args, **kwargs):
        if not self.pk:
            # Generate a new UUID for a new instance of the model
            while True:
                uuid = generate_uuid()
                if not CountyGovernment.objects.filter(code=uuid).exists():
                    self.code = uuid
                    break

        return super().save(*args, **kwargs)


class Aggregator(models.Model):
    user = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.CASCADE)
    code = models.CharField(max_length=20, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    county = models.ForeignKey(County, blank=True, null=True, on_delete=models.SET_NULL)
    county_number = models.IntegerField(blank=True, null=True, default=0)
    mobile_number = models.CharField(max_length=30, blank=True, null=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    created_on = models.DateTimeField(auto_now=True, auto_created=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            # Set the county on save if given the county_number
            county = County.objects.filter(
                county_number=self.county_number).first()
            self.county = county if self.county is None else self.county
            # Generate a new UUID for a new instance of the model
            while True:
                uuid = generate_uuid()
                if not Aggregator.objects.filter(code=uuid).exists():
                    self.code = uuid
                    break

        return super().save(*args, **kwargs)

 
class CollectionCenter(models.Model):
    county = models.ForeignKey(
        County, blank=True, null=True, on_delete=models.SET_NULL)
    sub_county = models.CharField(max_length=100, blank=True, null=True)
    code = models.CharField(max_length=20, blank=True, null=True)
    name = models.CharField(max_length=512, blank=False, null=False)
    grade_1 = models.IntegerField(blank=True, null=True)
    price_for_grade_1 = models.IntegerField(blank=True, null=True)
    grade_2 = models.IntegerField(blank=True, null=True)
    price_for_grade_2 = models.IntegerField(blank=True, null=True)
    grade_3 = models.IntegerField(blank=True, null=True)
    price_for_grade_3 = models.IntegerField(blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)
    contact_person_name = models.CharField(max_length=200, blank=True, null=True)
    contact_person_phone_number = models.CharField(max_length=13, blank=True, null=True)
    created_on = models.DateTimeField(auto_created=True, auto_now_add=True)
    lat = models.CharField(max_length=512, blank=False, null=False)
    lon = models.CharField(max_length=512, blank=False, null=False)

    flashsale = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now=True, auto_created=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)

        if not self.pk:
            # Generate a new UUID for a new instance of the model
            while True:
                uuid = generate_uuid()
                if not CollectionCenter.objects.filter(code=uuid).exists():
                    self.code = uuid
                    break

        return super().save(*args, **kwargs)


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    message = models.TextField()

    created_on = models.DateTimeField(auto_now=True, auto_created=True)

    def __str__(self):
        return self.subject


@receiver(post_save, sender=Contact)
def send_contact_creation_email(sender, instance, created, **kwargs):
    """
    This signal listens for contact form creation and fires to send an email to the admin
    """
    if created:
        send_custom_email('contact_email', instance, settings.ADMIN_EMAILS)
        return True
    