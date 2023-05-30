from django.db import models
from django.contrib.auth.models import User
from mainapp.models import County
from django.template.defaultfilters import slugify

import random
import string


def generate_uuid(length=6):
    """
    Generate a random UUID consisting of 5 uppercase letters and numbers.
    """
    characters = string.ascii_uppercase + string.digits
    uuid = ''.join(random.choice(characters) for _ in range(length))
    return uuid


# Create your models here.
FILE_CHOICES = (
    ('pdf', 'Pdf'),
    ('doc', 'Doc'),
    ('video', 'Video'),
    ('image', 'image'),
)


class Event(models.Model):
    created_by = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, blank=False, null=False)
    county_number = models.IntegerField(blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)
    description = models.TextField()
    venue = models.CharField(max_length=150)
    image = models.ImageField(upload_to='events/images/')
    date = models.DateField()

    created_on = models.DateTimeField(auto_created=True, auto_now_add=True)
    updated_on = models.DateTimeField(auto_created=True, auto_now=True)

    class Meta:
        verbose_name_plural = 'Events'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super(Event, self).save(*args, **kwargs)


class FarmerGroup(models.Model):
    created_by = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.CASCADE)
    code = models.CharField(max_length=30, blank=True, null=True)
    county_number = models.IntegerField(blank=True, null=True)
    county = models.ForeignKey(
        County, blank=True, null=True, on_delete=models.SET_NULL, related_name="farmer_groups")
    title = models.CharField(max_length=100, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    location = models.CharField(
        default="", max_length=50, blank=True, null=True)
    image = models.ImageField(
        upload_to='stakeholders/farmer-groups/', blank=True, null=True)

    created_on = models.DateTimeField(auto_created=True, auto_now_add=True)
    updated_on = models.DateTimeField(auto_created=True, auto_now=True)

    class Meta:
        verbose_name_plural = 'Farmer Groups'

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        if not self.pk:
            # Generate a new UUID for a new instance of the model
            while True:
                uuid = generate_uuid()
                if not FarmerGroup.objects.filter(code=uuid).exists():
                    self.code = uuid
                    break

        return super().save(*args, **kwargs)


class ExtensionService(models.Model):
    created_by = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.CASCADE)
    code = models.CharField(max_length=30, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    county = models.ForeignKey(
        County, blank=True, null=True, on_delete=models.SET_NULL)
    description = models.TextField()
    image = models.ImageField(upload_to='stakeholders/farmer-groups/')

    created_on = models.DateTimeField(auto_created=True, auto_now_add=True)
    updated_on = models.DateTimeField(auto_created=True, auto_now=True)

    class Meta:
        verbose_name_plural = 'Extension Services'

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if not self.pk:
            # Generate a new UUID for a new instance of the model
            while True:
                uuid = generate_uuid()
                if not ExtensionService.objects.filter(code=uuid).exists():
                    self.code = uuid
                    break

        return super().save(*args, **kwargs)


class Nursery(models.Model):
    created_by = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=512, blank=False, null=True)
    county = models.ForeignKey(
        County, blank=True, null=True, on_delete=models.SET_NULL)
    county_number = models.IntegerField(blank=True, null=True)

    number_of_seedlings_received = models.IntegerField(
        blank=True, null=True, help_text='This is for nurseries')
    number_of_seedlings_distributed = models.IntegerField(
        blank=True, null=True, help_text='This is for nurseries')
    number_of_seedlings_availaible = models.IntegerField(
        blank=True, null=True, help_text='This is for nurseries')

    lat = models.CharField(max_length=512, blank=False, null=True)
    lon = models.CharField(max_length=512, blank=False, null=True)

    slug = models.SlugField(blank=True, null=True)
    contact_person_name = models.CharField(
        max_length=200, blank=True, null=True)
    contact_person_phone_number = models.IntegerField(blank=True, null=True)
    created_on = models.DateTimeField(auto_created=True, auto_now_add=True)
    updated_on = models.DateTimeField(auto_created=True, auto_now=True)

    class Meta:
        verbose_name_plural = 'Nurseries'

    def __str__(self) -> str:
        return self.name


class DemoFarm(models.Model):
    created_by = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=512, blank=False, null=True)
    county = models.ForeignKey(
        County, blank=True, null=True, on_delete=models.SET_NULL)
    county_number = models.IntegerField(blank=True, null=True)

    number_of_seedlings_planted = models.IntegerField(blank=True, null=True)
    size_of_demo_farm = models.FloatField(blank=True, null=True)
    number_of_farmers_trained = models.IntegerField(blank=True, null=True)

    lat = models.CharField(max_length=512, blank=False, null=True)
    lon = models.CharField(max_length=512, blank=False, null=True)

    slug = models.SlugField(blank=True, null=True)
    contact_person_name = models.CharField(
        max_length=200, blank=True, null=True)
    contact_person_phone_number = models.IntegerField(blank=True, null=True)

    created_on = models.DateTimeField(auto_created=True, auto_now_add=True)
    updated_on = models.DateTimeField(auto_created=True, auto_now=True)

    class Meta:
        verbose_name_plural = 'Demo Farms'

    def __str__(self) -> str:
        return self.name


class Knowledge_base(models.Model):
    created_by = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.CASCADE)
    county = models.ForeignKey(
        County, blank=True, null=True, on_delete=models.SET_NULL)
    sub_county = models.CharField(max_length=100, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField()
    # image = models.ImageField(upload_to="posts/images/", blank=True, null=True)
    file = models.FileField(
        upload_to="resources/videos/", blank=True, null=True)
    file_type = models.CharField(
        choices=FILE_CHOICES, max_length=20, blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)

    created_on = models.DateTimeField(auto_created=True, auto_now_add=True)
    updated_on = models.DateTimeField(auto_created=True, auto_now=True)
 
    class Meta:
        verbose_name_plural = 'Knowledge Base'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super(Knowledge_base, self).save(*args, **kwargs)


class Post(models.Model):
    created_by = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.SET_NULL)
    title = models.TextField(blank=False, null=True)
    slug = models.SlugField(blank=True, null=True)
    message = models.TextField()

    image = models.ImageField(upload_to="posts/images/", blank=True, null=True)
    video = models.FileField(upload_to="posts/videos/", blank=True, null=True)

    created_on = models.DateTimeField(auto_created=True, auto_now_add=True)
    updated_on = models.DateTimeField(auto_created=True, auto_now=True)

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super(Post, self).save(*args, **kwargs)


class Reply(models.Model):
    created_by = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.SET_NULL)
    post = models.ForeignKey(Post, blank=True, null=True,
                             on_delete=models.CASCADE, related_name="replies")
    reply = models.TextField()

    created_on = models.DateTimeField(auto_created=True, auto_now_add=True)
    updated_on = models.DateTimeField(auto_created=True, auto_now=True)

    def __str__(self):
        return self.reply
