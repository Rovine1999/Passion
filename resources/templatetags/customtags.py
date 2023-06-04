import json
from urllib.parse import urlparse, parse_qsl, urlencode

from django import template
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta

from giz_app.models import Enumerator, Company
from giz_app.serializers import CollectionCenterSerializer, UserSerializer
from interact.models import UserChatGroup
from resources.serializers import DemoFarmSerializer, NurserySerializer, FarmerGroupSerializer
from giz_app.models import Farmer, CollectionCenter, County
from resources.models import Nursery, DemoFarm, FarmerGroup
from django.urls import reverse
from resources.models import Event

register = template.Library()


@register.filter
def to_json(obj, target):
    serializer = None
    if target == 'demofarm':
        serializer = DemoFarmSerializer(obj, many=False)
    if target == 'nursery':
        serializer = NurserySerializer(obj, many=False)
    if target == 'collection-center':
        serializer = CollectionCenterSerializer(obj, many=False)
    if target == 'farmer-group':
        serializer = FarmerGroupSerializer(obj, many=False)
    return json.dumps(serializer.data if serializer else serializer)


@register.filter
def counties(text):
    return County.objects.all().order_by('order')


@register.filter
def filter_nurseries_per_county(county_id):
    return Nursery.objects.filter(county__id=county_id)


@register.filter
def filter_demofarms_per_county(county_id):
    return DemoFarm.objects.filter(county__id=county_id)


@register.filter
def filter_collection_centers_per_county(county_id):
    return CollectionCenter.objects.filter(county__id=county_id)


@register.filter
def update_county_param(path, county):
    parsed_url = urlparse(path)
    query_params = dict(parse_qsl(parsed_url.query))
    query_params['county'] = county
    new_query_string = urlencode(query_params)
    new_path = parsed_url.path + '?' + new_query_string if new_query_string else parsed_url.path
    return new_path


@register.filter
def farmer_groups(txt):
    return FarmerGroup.objects.get_queryset()


@register.filter
def chat_rooms(user):
    qlookup1 = Q(user_1__id=user.id) | Q(user_2__id=user.id)
    chat_rooms_ = UserChatGroup.objects.filter(qlookup1)
    return chat_rooms_


@register.filter
def get_other_user(chat_room, user_id):
    return backend_get_other_user(chat_room, user_id)


@register.filter
def get_user_type(user):
    return backend_get_user_type(user)


@register.filter
def get_chat_room_data(chat_room, user_id):
    other_user = backend_get_other_user(chat_room, user_id)
    user_type = backend_get_user_type(other_user)
    other_user_data = UserSerializer(other_user).data
    obj = {
        "chat_name": chat_room.chat_name,
        "chat_id": chat_room.id,
        "full_name": f"{other_user.first_name} {other_user.last_name}",
        "user_type": user_type,
        "profile_photo": other_user_data['profile']['profile_photo'],
        "my_user_id": user_id
    }
    return json.dumps(obj)


def backend_get_other_user(chat_room, user_id):
    if chat_room.user_1.id == user_id:
        return chat_room.user_2
    return chat_room.user_1


def backend_get_user_type(user):
    farmer = getattr(user, 'farmer', None)
    aggregator = getattr(user, 'aggregator', None)
    financial_provider = getattr(user, 'financialprovider', None)
    insurance_provider = getattr(user, 'insuranceprovider', None)
    transport_logistics = getattr(user, 'transportlogistics', None)
    county_govt = getattr(user, 'countygovernment', None)
    coperative = getattr(user, 'coperatives', None)
    inputsuppliersandagrovets = getattr(user, 'inputsuppliersandagrovets', None)
    processors = getattr(user, 'processors', None)
    if farmer:
        return "Farmer"
    if aggregator:
        return "Aggregator"
    if financial_provider:
        return "Financial Provider"
    if insurance_provider:
        return "Insurance Provider"
    if transport_logistics:
        return "Transport & Logistics"
    if county_govt:
        return "County Government"
    if coperative:
        return "Coperative"
    if inputsuppliersandagrovets:
        return "Input Supplier & Aggrovet"
    if processors:
        return "Processor"
    return "Not Categorized"


@register.filter
def get_model_entries(model):
    if model == 'enumerator':
        return Enumerator.objects.all()
    if model == 'company':
        return Company.objects.all()
    if model == 'counties':
        return County.objects.all()
    if model == 'farmer_groups':
        return FarmerGroup.objects.all()
    return []


@register.filter
def get_full_url(url_name):
    return reverse(url_name)


@register.filter
def match_paths(path, view_name):
    if path == reverse(view_name):
        return True
    return False


def sidebar_link(label, url_name, icon):
    return {
        "label": label,
        "url_name": url_name,
        "icon": icon,
        "full_url": reverse(url_name)
    }


@register.filter
def admin_sidebar_urls(links):
    sidebar_links = [
        sidebar_link("Enumerators", "dashboard-resources-enumerators", "support_agent"),
        sidebar_link("Farmers", "dashboard-farmers", "people"),
        sidebar_link("Demo Farms", "dashboard-resources-demofarms", "broken_image"),
        sidebar_link("Nurseries", "dashboard-resources-nurseries", "nature"),
        sidebar_link("Collection Centers", "dashboard-resources-collection", "emoji_transportation"),
        sidebar_link("Farmer Groups", "dashboard-resources-farmergroups", "diversity_2"),
        sidebar_link("Aggregators", "dashboard-resources-aggregators", "group"),
        sidebar_link("Offtaker", "dashboard-resources-offtakers", "local_shipping"),
        sidebar_link("Extension Services", "dashboard-resources-extensionservices", "extension"),
        sidebar_link("Events", "dashboard-resources-events", "event"),
        sidebar_link("Posts", "dashboard-resources-posts", "post_add"),
        sidebar_link("Processors", "dashboard-resources-processors", "memory"),
    ]

    return sidebar_links


@register.filter
def providers(providers_):
    return get_providers()


def get_providers():
    all_providers = [
        {'label': 'Cooperatives', 'value': 'Coperatives'},
        {'label': 'Processors', 'value': 'Processors'},
        {'label': 'Input Suppliers', 'value': 'InputSuppliersAndAgrovets'},
        {'label': 'Financial Providers', 'value': 'FinancialProvider'},
        {'label': 'Insurance Providers', 'value': 'InsuranceProvider'},
        {'label': 'County Government', 'value': 'CountyGovernment'},
    ]
    return all_providers


@register.filter
def tokenize_date(date):
    # Extract the day, month, and year from the input date object
    day = date.day
    month = date.strftime('%B')
    year = date.year

    # Return a dictionary with the extracted values
    return {
        "day": day,
        "month": month,
        "year": year
    }


@register.filter
def multiply(a, b):
    result = float(a) * float(b)
    return "{:.2f}".format(result)


@register.simple_tag
def quick_stats():
    return {
        "farmers": Farmer.objects.count(),
        "demo_farms": DemoFarm.objects.count(),
        "collection_centers": CollectionCenter.objects.count(),
        "counties": County.objects.count(),
    }


@register.simple_tag
def events(events_type):
    if events_type == 'new_events':
        today = timezone.now().date()
        close_events_date = today + timedelta(days=3)
        return Event.objects.filter(date__gte=today).filter(date__lt=close_events_date)
    return []