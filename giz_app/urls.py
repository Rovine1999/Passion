from django.urls import path
from .views import *

urlpatterns = [
    # Farmers
    path('farmers/', farmers, name='farmers'),
    path('farmers/signup/', farmersignup, name='farmersignup'),
    path('farmers/nurseries/', nurseries, name='nurseries'),
    path('farmers/demonstration-farms/', demofarms, name='demofarms'),
    path('farmers/collection-centers/', collection, name='collection'),

    # Enumerators
    path('enumerators/signup', enumeratorsignup, name='enumeratorsignup'),

    # offtakers
    path('offtakers/', offtakers, name='offtakers'),
    path('offtakers/signup/', offtakersignup, name='offtakersignup'),
    path('offtakers/counties/<str:county_id>/<str:slug>/', singlecounty, name='county'),

    # stakeholders
    path('stakeholders/all-providers/', all_providers, name='all-providers'),
    path('stakeholders/provider/<str:provider>/', single_providers, name='single-provider'),

    path('aggregator/signup/', aggregator_signup, name='aggregator_signup'),

    # Service Providers
    path('provider/signup', service_provider_signup, name='service_provider_signup'),
    path('provider/signup/ajax/', service_provider_signup_ajax, name='service_provider_signup_ajax'),

    # Extension Services
    path('extension-services/', extension_services, name="extension-services"),
    path('extension-services/counties/<str:county_id>/<str:slug>/', single_county_extension_services,
         name='extension-services-county'),
]
