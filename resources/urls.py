from django.urls import path
from .views import *

urlpatterns = [
    path('events', events, name='events'),
    path('events/learn-more/<str:event_id>/<str:slug>/', single_event, name='single_event'),
    path('knowledgebase', knowledgebase, name='knowledgebase'),
    path('forums/', forums, name='forums'),
    path('farmers/groups/', farmergroups, name="farmergroups"),
    path('farmers/groups/county/<str:county_id>/<str:county_slug>/', farmergroups_county, name="farmergroups_county"),
]
