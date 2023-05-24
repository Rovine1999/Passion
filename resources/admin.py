from django.contrib import admin
from .models import *
# Register your models here.


admin.site.register(Event)
admin.site.register(FarmerGroup)
admin.site.register([Nursery, DemoFarm])
admin.site.register([Post, Reply])
admin.site.register(ExtensionService)
admin.site.register(Knowledge_base)
