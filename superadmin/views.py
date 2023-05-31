import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from giz_app.models import Farmer, CollectionCenter, Aggregator, Offtaker, Enumerator, Company
from django.contrib import messages
import openpyxl
from giz_app.serializers import FarmerSerializer
from mailer.utils import send_custom_email
from mainapp.models import County
from resources.models import Nursery, DemoFarm, FarmerGroup, Event, ExtensionService, Post
from giz_app.models import Processors
from django.db.models import Sum, Q, Count
from django.core import serializers
import random
from django.conf import settings


def is_not_blank_or_empty(my_str):
    return bool(my_str and my_str.strip())


# Create your views here.

def generate_colors(count):
    colors = ["#" + ''.join([random.choice('0123456789ABCDEF') for j in range(6)])
              for i in range(count)]
    return colors


def dashboard(request):
    farmers_ = Farmer.objects.all()

    groups = FarmerGroup.objects.annotate(num_farmers=Count('farmer'))
    groups_data_list = {
        "labels": [],
        "values": [],
    }
    for group in groups:
        groups_data_list["labels"].append(group.title)
        groups_data_list["values"].append(group.num_farmers)

    farmers_per_county = County.objects.annotate(num_farmers=Count('farmer'))
    colors = generate_colors(len(farmers_per_county))

    enumerators_ = Enumerator.objects.all()
    enumerators_stats = {
        "approved": enumerators_.filter(approved=True).count(),
        "unapproved": enumerators_.filter(approved=False).count(),
    }

    farmers_per_county_data_list = {
        "labels": [],
        "values": [],
        "colors": colors
    }
    for county in farmers_per_county:
        farmers_per_county_data_list["labels"].append(county.name)
        farmers_per_county_data_list["values"].append(county.num_farmers)

    context = {
        "users_total": User.objects.all().count(),
        "farmers_total": farmers_.count(),
        "male_farmers": farmers_.filter(user__profile__gender='male').count(),
        "female_farmers": farmers_.filter(user__profile__gender='female').count(),
        "demofarms_total": DemoFarm.objects.all().count(),
        "nurseries_total": Nursery.objects.all().count(),
        "collectioncenters_total": CollectionCenter.objects.all().count(),
        "farmergroups_total": FarmerGroup.objects.all().count(),
        "aggregators_total": Aggregator.objects.all().count(),
        "offtakers_total": Offtaker.objects.all().count(),

        "enumerators_total": enumerators_.count(),
        "enumerator_stats": json.dumps(enumerators_stats),

        "extension_services_total": ExtensionService.objects.all().count(),

        "events_total": Event.objects.all().count(),
        "posts_total": Post.objects.all().count(),
        "processors": Processors.objects.all().count(),

        # Chart js data
        "groups_data": json.dumps(groups_data_list),
        "farmers_per_county": json.dumps(farmers_per_county_data_list),
    }

    return render(request, template_name='super-admin/index.html', context=context)


def farmers(request):
    farmers_ = Farmer.objects.get_queryset().order_by('id')

    gender = request.GET.get('gender', None)
    status = request.GET.get('status', None)

    county = request.GET.get('county', None)
    location = request.GET.get('location', None)

    farmer_group = request.GET.get('farmer_group', None)

    ordering = request.GET.get('ordering', None)
    search = request.GET.get('search', None)

    if is_not_blank_or_empty(gender):
        farmers_ = farmers_.filter(user__profile__gender=gender)

    if is_not_blank_or_empty(status):
        farmers_ = farmers_.filter(user__is_active=status)

    if is_not_blank_or_empty(county):
        farmers_ = farmers_.filter(user__profile__county__id=county)

    if is_not_blank_or_empty(farmer_group):
        farmers_ = farmers_.filter(farmer_group__id=farmer_group)

    if is_not_blank_or_empty(search):
        farmers_ = farmers_.filter(Q(user__first_name__icontains=search)
                                   | Q(user__last_name__icontains=search)
                                   | Q(user__username__icontains=search)
                                   | Q(user__email__icontains=search)
                                   | Q(user__profile__phone_number__icontains=search)
                                   | Q(user__profile__alt_phone_number__icontains=search)
                                   | Q(landmark__icontains=search)
                                   | Q(farmer_number__icontains=search)
                                   | Q(coperatives__code__icontains=search)
                                   | Q(coperatives__company_name__icontains=search)
                                   | Q(coperatives__description__icontains=search)
                                   )

    if is_not_blank_or_empty(ordering):
        farmers_ = farmers_.order_by(ordering)

    paginator = Paginator(farmers_, 25)  # Show 25 farmers per page.

    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "pages": paginator.page_range,
        "page_count": paginator.num_pages,
        "farmers_total": farmers_.count(),
    }
    return render(request, template_name='super-admin/pages/farmers/farmers.html', context=context)


def upload_farmers(request):
    context = {}
    if request.method == "POST":
        excel_file = request.FILES.get("csv")
        enumerator = request.POST.get("enumerator", None)

        if enumerator == "" or enumerator is None:
            messages.info(request, "Please select an enumerator")
            return redirect(request.META['HTTP_REFERER'])

        # enumerator_ = Enumerator.objects.filter(id=enumerator).first()

        wb = openpyxl.load_workbook(excel_file)
        excel_data = list()

        for letter in ["Sheet1"]:
            worksheet = wb[letter]
            for row in worksheet.iter_rows():
                row_data = list()
                for cell in row:
                    row_data.append(str(cell.value))
                excel_data.append(row_data)
        entries = []
        for i, data in enumerate(excel_data):
            if i != 0:
                # "postal_address": data[7],
                farmer = {
                    "user": {
                        "first_name": data[0],
                        "last_name": data[1],
                        "username": data[2],
                        "profile": {
                            "phone_number": data[3],
                            "gender": data[5],
                            # "year_of_birth": data[4],
                            # "county": int(data[6]) if data[6].isdecimal() else None,
                            # "id_number": data[5]
                        },
                    },
                    "county_number": int(data[8]) if data[8].isdecimal() else None,
                    "county_name": data[6],
                    "sub_county": data[7],
                    "acreage": data[9],
                    "enumerator_code": data[10],
                    "enumerator": enumerator,
                    # "farmer_number": data[13],
                    # "landmark": data[14],
                    "selling_place": data[11],
                    "farmer_group_code": data[12],
                }
                entries.append(farmer)

        for farmer_entry in entries:
            serializer = FarmerSerializer(data=farmer_entry, many=False)
            if serializer.is_valid():
                data = serializer.save()
                messages.success(request, f"{data.user.first_name} {data.user.last_name} "
                                          f"- Uploaded successfully")
            else:
                data = serializer.data
                messages.error(request, f"Upload failed for {data['user']['first_name']} {data['user']['last_name']} "
                                        f" - "
                                        f"{json.dumps(serializer.errors)}")
    return render(request, template_name="super-admin/pages/farmers/upload-farmers.html", context=context)


def demo_farms(request):
    demo_farms_ = DemoFarm.objects.all()
    paginator = Paginator(demo_farms_, 10)  # Show 25 farmers per page.

    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "pages": paginator.page_range,
        "page_count": paginator.num_pages,
        "farmers_total": demo_farms_.count(),
    }
    return render(request, template_name='super-admin/pages/resources/demofarms.html', context=context)


def nurseries(request):
    nurseries_ = Nursery.objects.all()
    paginator = Paginator(nurseries_, 25)  # Show 25 farmers per page.

    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "pages": paginator.page_range,
        "page_count": paginator.num_pages,
        "farmers_total": nurseries_.count(),
    }
    return render(request, template_name='super-admin/pages/resources/nurseries.html', context=context)


def collection(request):
    collection_ = CollectionCenter.objects.all()
    paginator = Paginator(collection_, 25)  # Show 25 farmers per page.

    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "pages": paginator.page_range,
        "page_count": paginator.num_pages,
        "farmers_total": collection_.count(),
    }
    return render(request, template_name='super-admin/pages/resources/collection.html', context=context)


def farmergroups(request):
    farmergroups_ = FarmerGroup.objects.all()
    paginator = Paginator(farmergroups_, 25)  # Show 25 farmers per page.

    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "pages": paginator.page_range,
        "page_count": paginator.num_pages,
        "farmers_total": farmergroups_.count(),
    }
    return render(request, template_name='super-admin/pages/resources/farmergroups.html', context=context)


def aggregators(request):
    aggregators_ = Aggregator.objects.all()
    paginator = Paginator(aggregators_, 25)  # Show 25 farmers per page.

    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "pages": paginator.page_range,
        "page_count": paginator.num_pages,
        "farmers_total": aggregators_.count(),
    }
    return render(request, template_name='super-admin/pages/resources/aggregators.html', context=context)


def offtakers(request):
    offtakers_ = Offtaker.objects.all()
    paginator = Paginator(offtakers_, 25)  # Show 25 farmers per page.

    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "pages": paginator.page_range,
        "page_count": paginator.num_pages,
        "farmers_total": offtakers_.count(),
    }
    return render(request, template_name='super-admin/pages/resources/offtakers.html', context=context)


def enumerators(request):
    enumerators_ = Enumerator.objects.all()

    gender = request.GET.get('gender', None)
    approved = request.GET.get('approved', None)

    county = request.GET.get('county', None)

    ordering = request.GET.get('ordering', None)
    search = request.GET.get('search', None)

    if is_not_blank_or_empty(gender):
        enumerators_ = enumerators_.filter(user__profile__gender=gender)

    if is_not_blank_or_empty(approved):
        enumerators_ = enumerators_.filter(approved=approved)

    if is_not_blank_or_empty(county):
        enumerators_ = enumerators_.filter(user__profile__county__id=county)

    if is_not_blank_or_empty(search):
        enumerators_ = enumerators_.filter(Q(user__first_name__icontains=search)
                                           | Q(user__last_name__icontains=search)
                                           | Q(user__username__icontains=search)
                                           | Q(user__email__icontains=search)
                                           | Q(user__profile__phone_number__icontains=search)
                                           | Q(user__profile__alt_phone_number__icontains=search)
                                           | Q(phone_number__icontains=search)
                                           )

    if is_not_blank_or_empty(ordering):
        enumerators_ = enumerators_.order_by(ordering)

    paginator = Paginator(enumerators_, 25)  # Show 25 farmers per page.

    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "pages": paginator.page_range,
        "page_count": paginator.num_pages,
        "farmers_total": enumerators_.count(),
    }
    return render(request, template_name='super-admin/pages/resources/enumerators.html', context=context)


def extensionservices(request):
    extensionservices_ = ExtensionService.objects.all()
    paginator = Paginator(extensionservices_, 25)  # Show 25 farmers per page.

    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "pages": paginator.page_range,
        "page_count": paginator.num_pages,
        "farmers_total": extensionservices_.count(),
    }
    return render(request, template_name='super-admin/pages/resources/extension.html', context=context)


def events(request):
    events_ = Event.objects.all()
    paginator = Paginator(events_, 25)  # Show 25 farmers per page.

    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "pages": paginator.page_range,
        "page_count": paginator.num_pages,
        "farmers_total": events_.count(),
    }
    return render(request, template_name='super-admin/pages/resources/events.html', context=context)


def posts(request):
    posts_ = Post.objects.all()
    paginator = Paginator(posts_, 25)  # Show 25 farmers per page.

    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "pages": paginator.page_range,
        "page_count": paginator.num_pages,
        "farmers_total": posts_.count(),
    }
    return render(request, template_name='super-admin/pages/resources/posts.html', context=context)


def processors(request):
    processors_ = Processors.objects.all()
    paginator = Paginator(processors_, 25)  # Show 25 farmers per page.

    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "pages": paginator.page_range,
        "page_count": paginator.num_pages,
        "farmers_total": processors_.count(),
    }
    return render(request, template_name='super-admin/pages/resources/processors.html', context=context)


def approve_company(request, company_id):
    if request.method == "POST":
        company = get_object_or_404(Company, id=company_id)
        company.approved = True
        company.save()
        messages.success(request, "The company has been approved")
    return redirect(request.META['HTTP_REFERER'])


def approve_enumerator(request, enumerator_id):
    if request.method == "POST":
        enumerator = get_object_or_404(Enumerator, id=enumerator_id)
        enumerator.approved = True
        enumerator.save()
        messages.success(request, "The Enumerator has been approved")
        send_custom_email('enumerator_approved', enumerator, [enumerator.user.email] + settings.ADMIN_EMAILS)
    return redirect(request.META['HTTP_REFERER'])

