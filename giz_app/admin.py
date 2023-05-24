from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Profile)
admin.site.register(Farmer)
admin.site.register(Offtaker)
admin.site.register(Enumerator)
admin.site.register(Coperatives)
admin.site.register(Aggregator)
admin.site.register([Contact, CollectionCenter])
admin.site.register(Company)

admin.site.register([Processors, InsuranceProvider, FinancialProvider, TransportLogistics, InputSuppliersAndAgrovets,
                     CountyGovernment])
