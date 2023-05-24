import json

from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator

from resources.templatetags.customtags import get_providers
from .models import *
from django.db.models import Q
from django.contrib import messages

from resources.models import *
from .serializers import ProcessorSerializer, CountyGovernmentSerializer, \
    InsuranceProviderSerializer, FinancialProviderSerializer, InputSuppliersAndAgrovetsSerializer, \
    TransportLogisticSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.apps import apps


def farmers(request):
    farmers_ = Farmer.objects.all()
    paginator = Paginator(farmers_, 25)  # Show 25 farmers per page.

    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "pages": paginator.page_range,
        "page_count": paginator.num_pages,
        "farmers_total": paginator.count,
    }
    return render(request, template_name='agrul/pages/farmers/farmers.html', context=context)


def farmersignup(request):
    context = {}
    return render(request, template_name='agrul/pages/farmers/farmer-signup.html', context=context)


def enumeratorsignup(request):
    context = {}
    return render(request, template_name='agrul/pages/enumerators/enumerator-signup.html', context=context)


def aggregator_signup(request):
    return render(request, template_name='agrul/pages/aggregators/aggregator-signup.html', context={})


def offtakers(request):
    context = {
        'counties': County.objects.all()
    }
    return render(request, template_name='offtakers/offtakers.html', context=context)


def offtakersignup(request):
    counties = County.objects.all()
    if request.method == 'POST':
        request.POST._mutable = True
        request.POST.update({"username": request.POST.get("email")})
        request.POST._mutable = False
        user = createuser(request)
        vehicle_number = request.POST.get('vehicle_number')
        location = request.POST.get('location')
        offtaker = Offtaker(vehicle_number=vehicle_number, location=location)
        if user['message'] is None:
            # Create farmer user profile
            user_ = user['user']
            user_.save()
            user_.set_password(user['user'].password)
            user_.save()
            user_.refresh_from_db()
            saveuserprofile(user_, user['profile'])

            # Create farmer profile
            offtaker.user = user_
            offtaker.save()
            return redirect('login')
        else:
            messages.warning(request, user['message'])
            return render(request, template_name='registration/offtakerreg.html',
                          context={"user": user, 'offtakerdetails': offtaker,
                                   'counties': counties})

    return render(request, template_name='registration/offtakerreg.html', context={'counties': counties})


def service_provider_signup(request):
    context = {
        'providers': [
            {'value': 'processor', 'label': 'Processor'},
            {'value': 'transport_and_logistics', 'label': 'Transport & Logistics'},
            {'value': 'input_supplier_and_agrovets',
                'label': 'Input Supplier & Aggrovet'},
            {'value': 'financial_provider', 'label': 'Financial Provider'},
            {'value': 'insurance_provider', 'label': 'Insurance Provider'},
            {'value': 'county_government', 'label': 'County Government'},
            {'value': 'coperatives', 'label': 'Cooperative'},
        ]
    }
    return render(request, template_name="agrul/pages/providers/provider-signup.html", context=context)


@api_view(['POST'])
def service_provider_signup_ajax(request):
    if request.method == 'POST':
        request.POST._mutable = True
        request.POST['user.profile.profile_photo'] = request.FILES.get(
            'profile_photo')
        request.POST['image'] = request.FILES.get('image')
        request.POST._mutable = False
        serializer = None

        provider = request.POST.get('provider')
        if provider == 'processor':
            serializer = ProcessorSerializer(data=request.POST)

        if provider == 'transport_and_logistics':
            serializer = TransportLogisticSerializer(data=request.POST)

        if provider == 'input_supplier_and_agrovets':
            serializer = InputSuppliersAndAgrovetsSerializer(data=request.POST)

        if provider == 'financial_provider':
            serializer = FinancialProviderSerializer(data=request.POST)

        if provider == 'insurance_provider':
            serializer = InsuranceProviderSerializer(data=request.POST)

        if provider == 'county_government':
            serializer = CountyGovernmentSerializer(data=request.POST)

        if provider == 'coperatives':
            serializer = CountyGovernmentSerializer(data=request.POST)

        if serializer is not None:
            if serializer.is_valid():
                messages.success(request, "Sign Up successful")
                serializer.save()
                # return redirect('login')
                return Response(data=serializer.data, status=201)
            else:
                return Response(data=serializer.errors)
        else:
            messages.error(request, "Something went wrong", extra_tags='danger')
            return Response(data={'provider': ['provider type not selected']})
    return Response(data={'method': ['Get method not allowed']})


def singlecounty(request, county_id, slug):
    county = get_object_or_404(County, id=county_id)
    ccs = CollectionCenter.objects.filter(county=county)

    context = {
        'county': county,
        'collection_centers': ccs,
        'nursery_markers': json.dumps(
            [[center.name, center.lat, center.lon] for center in ccs]
        ),
        # 'nursery_markers_info': json.dumps(
        #     [[center.description] for center in ccs]
        # )
    }

    return render(request, template_name='offtakers/singlecounty.html', context=context)


def createuser(request):
    # ID_NUMBER FOR FARMER, EMAIL FOR ADMIN OR USERNAME
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    email = request.POST.get('email')
    password1 = request.POST.get('password1')
    password2 = request.POST.get('password2')

    # Userprofile
    address = request.POST.get('address')
    id_number = request.POST.get('id_number')
    county = request.POST.get('county')
    phone_number = request.POST.get('phone_number')
    alt_phone_number = request.POST.get('alt_phone_number', None)
    profile_photo = request.FILES.get('profile_photo')
    year_of_birth = request.POST.get('year_of_birth')
    gender = request.POST.get('gender')

    user = User(username=phone_number, first_name=first_name,
                last_name=last_name, email=email, password=password1)

    userprofile = Profile(user=user, address=address, id_number=id_number,
                          phone_number=phone_number,
                          profile_photo=profile_photo, year_of_birth=year_of_birth, gender=gender)

    user_ = User.objects.filter(
        Q(username=phone_number) | Q(email=email)).first()
    if user_ is not None:
        if password1 != password2:
            return {"message": "password mismatch", "user": user, "profile": userprofile}

        return {"message": "User with same credentials already exists", "user": user, "profile": userprofile}

    return {"message": None, "user": user,
            "profile": userprofile}


def nurseries(request):
    data = Nursery.objects.all()
    context = {
        'nurseries': data,
        'nursery_data_markers': json.dumps(
            [[center.name, center.lat, center.lon] for center in data]
        ),
        'nursery_data_markers_info': json.dumps(
            [[""] for center in data]
        )
    }
    return render(request, template_name='agrul/pages/farmers/nurseries.html', context=context)


def demofarms(request):
    data = DemoFarm.objects.all()
    context = {
        'demofarms': data,
        'demofarms_data_markers': json.dumps(
            [[center.name, center.lat, center.lon] for center in data]
        ),
        'demofarms_data_markers_info': json.dumps(
            [[""] for center in data]
        ),
    }
    return render(request, template_name='agrul/pages/farmers/demofarms.html', context=context)


def collection(request):
    context = {
        'collection_centers': CollectionCenter.objects.all()
    }
    return render(request, template_name='agrul/pages/farmers/collection-centers.html', context=context)


def saveuserprofile(user, profile):
    user.profile.address = profile.address
    user.profile.phone_number = profile.phone_number
    user.profile.alt_phone_number = profile.alt_phone_number
    user.profile.county = profile.county
    user.profile.profile_photo = profile.profile_photo
    user.profile.age = profile.age
    user.profile.gender = profile.gender
    user.profile.save()


def extension_services(request):
    context = {
        'counties': County.objects.all(),
    }
    return render(request, template_name='extension-services/extension-services.html', context=context)


def single_county_extension_services(request, county_id, slug):
    county = get_object_or_404(County, id=county_id)

    context = {
        "county": county,
        "extension_services": ExtensionService.objects.filter(county=county)
    }

    return render(request, template_name='extension-services/singlecounty.html', context=context)


def all_providers(request):
    context = {
        "financial_providers": FinancialProvider.objects.get_queryset(),
        "insurance_providers": InsuranceProvider.objects.get_queryset(),
        "transport_providers": TransportLogistics.objects.get_queryset(),
        "county_providers": CountyGovernment.objects.get_queryset(),
        "cooperative_providers": Coperatives.objects.get_queryset(),
        "input_providers": InputSuppliersAndAgrovets.objects.get_queryset(),
        "processor_providers": Processors.objects.get_queryset(),
        "aggregators": Aggregator.objects.get_queryset()
    }
    return render(request, template_name='agrul/pages/providers/provider_users.html', context=context)


def single_providers(request, provider):

    provider_ = None
    for prov in get_providers():
        if prov['value'] == provider:
            provider_ = prov

    Model = apps.get_model(app_label='giz_app', model_name=provider)
    objects = None
    if Model:
        objects = Model.objects.all()
    context = {
        'providers': objects,
        'title': provider_['label']
    }
    return render(request, template_name='agrul/pages/providers/providers.html', context=context)
