from django.contrib import admin
from .models import AppConfig, Subscriber, County
# Register your models here.

admin.site.register([AppConfig, Subscriber, County])
