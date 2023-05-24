import sys
import traceback

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from giz_app.forms import CreateUserForm
from giz_app.models import Contact, County, Profile
from mailer.views import send_contact_us_email, send_subscription_confirmation_email
from shop.models import Order
import logging

from django.contrib.auth.models import Group, User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.utils import timezone
from resources.models import Event
from datetime import timedelta
from django.db.models import Q

from django.core.mail import send_mail
from .forms import SubscriptionForm
from .models import Subscriber

from shop.models import Product
from giz_app.models import Farmer, Offtaker, Processors, Aggregator, CollectionCenter
from resources.models import FarmerGroup

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from mailer.utils import send_custom_email

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Subscriber)
def send_subscriber_creation_email(sender, instance, created, **kwargs):
    """
    This signal listens for company creation and fires sending a company creation email
    """
    if created:
        send_custom_email('subscription_confirmation', instance, [instance.email] + settings.ADMIN_EMAILS)
        return True


# Required for account profile
def account_profile(request):
    context = {
        "orders": Order.objects.filter(user=request.user).order_by('-id')
    }
    # return render(request, template_name='account/profile.html', context=context)
    return render(request, template_name='agrul/pages/account/profile.html', context=context)


# Required for orders
def account_orders(request):
    context = {
        "orders": Order.objects.filter(user=request.user).order_by('-id')
    }
    # return render(request, template_name='account/orders.html', context=context)
    return render(request, template_name='agrul/pages/account/orders.html', context=context)


# Required for homepage
def home(request):
    # user = User.objects.create(username="Rovine")
    # user.set_password("Rovine")
    # user.is_staff = True
    # user.is_superuser = True
    # user.is_active = True
    # user.save()

    today = timezone.now().date()
    close_events_date = today + timedelta(days=3)
    context = {
        "new_events": Event.objects.filter(date__gte=today).filter(date__lt=close_events_date),
        "counties": County.objects.all(),
        "featured_products": Product.objects.filter(featured=True)
    }
    # return render(request, template_name="index.html", context=context)
    return render(request, template_name="agrul/pages/index.html", context=context)


# Required for about page
def about(request):
    return render(request, template_name='agrul/pages/about-us.html', context={})


# Required for faq
def faq(request):
    return render(request, template_name='agrul/pages/faq.html', context={})


# Required to check for account approval
def check_approval(request, service_provider, additional_msg):
    failed = False
    username = request.POST.get('username', "")

    user_ = User.objects.filter(username=username).first()

    service_provider = getattr(user_, service_provider, None)
    if service_provider is not None:
        approved = service_provider.approved
        if not approved:
            messages.info(request, f"You must be approved as {additional_msg} to login. "
                                   "Contact support with your name and Email for a followup")
            failed = True

    return failed


# Required for login
def account_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        enumerator_failed = check_approval(request, 'enumerator', 'an enumerator')
        processor_failed = check_approval(request, 'processor', 'a processor')

        if enumerator_failed or processor_failed:
            return redirect(request.META['HTTP_REFERER'])
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'You have successfully logged In!')
            return redirect('home')
        else:
            messages.error(request, 'Login failed! Check your username and password.', extra_tags='danger')
            return redirect('login')

    return render(request, template_name='agrul/pages/auth/login.html', context={})


# Required for logout
def account_logout(request):
    logout(request)
    return redirect('home')


# Required for Contact page
def contactus(request):
    if request.method == "POST":
        contact_ = Contact(
            name=request.POST.get("name"),
            email=request.POST.get("email"),
            phone=request.POST.get("phone"),
            subject=request.POST.get("subject"),
            message=request.POST.get("message")
        )

        contact_.save()
        messages.success(request, "Message sent successfully.")
        send_contact_us_email(contact_)
    # return render(request, template_name='contactus.html', context={})
    return render(request, template_name='agrul/pages/contact-us.html', context={})


def subscribe(request):
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            subscriber = form.save()
            send_subscription_confirmation_email(subscriber)
            messages.info(request, 'Thank you for subscribing to our mailing list')
            return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('home')


def send_notifications(post_title, post_content):
    subscribers = Subscriber.objects.all()
    emails = [subscriber.email for subscriber in subscribers]
    message = f'New post: {post_title}\n\n{post_content}'
    send_mail(
        'New Post',
        message,
        'newpost@gizpassion.com',
        emails,
        fail_silently=False,
    )


def main_search(request):
    if request.method == 'POST':
        query = request.POST.get('query')
        sweet_passion = Product.objects.filter(product_tuype='sweet_passion').filter(
            Q(name__icontains=query) | Q(description__icontains=query))
        inputs = Product.objects.filter(product_tuype='input').filter(
            Q(name__icontains=query) | Q(description__icontains=query))
        other_fruits = Product.objects.filter(product_tuype='other_fruit').filter(
            Q(name__icontains=query) | Q(description__icontains=query))
        products = Product.objects.filter(product_tuype='product').filter(
            Q(name__icontains=query) | Q(description__icontains=query))

        farmer_groups = ''
        farmers = Farmer.objects.filter(village__icontains=query)
        processors = Processors.objects.filter(company_name__icontains=query)
        collection_centers = CollectionCenter.objects.filter(name__icontains=query)
        aggregators = Aggregator.objects.filter(name__icontains=query)
        offtakers = Offtaker.objects.filter(Q(name__icontains=query) | Q(vehicle_number__icontains=query))

        context = {

        }
        return render(request, template_name='', context=context)
    messages.warning(request, 'Only post requests allowed')
    return redirect(request.META.get('HTTP_REFERER'))


def error404(request, exception):
    page = ''
    if request.META.get('HTTP_REFERER'):
        page = request.META['HTTP_REFERER']
    # return render(request, template_name='errors/error404.html', context={'error_page': page, 'exception': exception})
    return render(request, template_name='agrul/pages/errors/404.html', context={'error_page': page, 'exception': exception})


def error500(request):
    exc_type, exc_value, tb = sys.exc_info()
    traceback_data = traceback.format_tb(tb)
    error_message = ''
    if len(traceback_data) > 0:
        error_message = f'''
            <h4>Error type </h4>
            <p>{exc_value}</p>
            <h4>Traceback</h4>
            <p>{traceback_data[0]}</p>
            <p>{traceback_data[1]}</p>
        '''
    return render(request, template_name='agrul/pages/errors/error500.html', context={"error_message": error_message})


# Required for geocoordinates page
def get_coordinates(request):
    return render(request, template_name='agrul/pages/coords/coords.html', context={})


def tcs(request):
    return render(request, template_name='agrul/pages/tcs.html', context={})

