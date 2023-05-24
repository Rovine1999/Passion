from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .models import *


def events(request):
    today = timezone.now().date()
    context = {
        "past_events": Event.objects.filter(date__lt=today),
        "upcoming_events": Event.objects.filter(date__gte=today),
    }
    return render(request, template_name='agrul/pages/resources/events.html', context=context)


def single_event(request, event_id, slug):
    event = get_object_or_404(Event, id=event_id)
    context = {
        "event": event
    }
    return render(request, template_name='resources/single_event.html', context=context)


def farmergroups(request):
    groups = FarmerGroup.objects.all()
    context = {
        'groups': groups
    }
    return render(request, template_name='agrul/pages/farmers/groups.html', context=context)


def farmergroups_county(request, county_id, county_slug):
    county = get_object_or_404(County, id=county_id)
    context = {
        "farmergroups": FarmerGroup.objects.filter(county=county),
        "county": county,
    }
    return render(request, template_name="stakeholders/farmergroups_county.html", context=context)


def knowledgebase(request):
    context = {
        "data": Knowledge_base.objects.all()
    }
    return render(request, template_name='agrul/pages/resources/knowledgebase.html', context=context)


def forums(request):
    return render(request, template_name='forums.html')
