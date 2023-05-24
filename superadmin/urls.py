from django.urls import path

from .views import *

urlpatterns = [
    path('', dashboard, name="dashboard"),
    path('farmers/', farmers, name="dashboard-farmers"),
    path('farmers/upload/', upload_farmers, name="dashboard-farmers-upload"),

    # Resources
    path('resources/demofarms/', demo_farms, name="dashboard-resources-demofarms"),
    path('resources/nurseries/', nurseries, name="dashboard-resources-nurseries"),
    path('resources/collection/', collection, name="dashboard-resources-collection"),
    path('resources/farmergroups/', farmergroups, name="dashboard-resources-farmergroups"),
    path('resources/aggregators/', aggregators, name="dashboard-resources-aggregators"),
    path('resources/offtakers/', offtakers, name="dashboard-resources-offtakers"),
    path('resources/enumerators/', enumerators, name="dashboard-resources-enumerators"),
    path('resources/extensionservices/', extensionservices, name="dashboard-resources-extensionservices"),
    path('resources/events/', events, name="dashboard-resources-events"),
    path('resources/posts/', posts, name="dashboard-resources-posts"),
    path('resources/processors/', processors, name="dashboard-resources-processors"),

    path('stakeholders/enumerators/approve/<str:enumerator_id>/', approve_enumerator, name="approve_enumerator")


]
