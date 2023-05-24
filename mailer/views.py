from django.core.mail import EmailMultiAlternatives, get_connection
from django.template import Template, Context
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import SearchFilter

from .models import EmailConfiguration, Email
from mainapp.models import AppConfig
from .serializers import EmailSerializer, EmailConfigSerializer

from giz_app.tokens import account_activation_token
from mainapp.extraclasses import StandardResultsSetPagination
from shop.models import Order
from shop.serializers import OrderSerializer
from .utils import send_email
from django.conf import settings


def sendepasswordresetmail(user, token):
    app_config = AppConfig.objects.filter(app="main").first()
    if user is not None and app_config is not None:
        email = app_config.reset_password_email
        email_config = app_config.reset_password_emailconfig

        email_template = Template(email.body)
        email_context = Context({'first_name': user.first_name,
                                 'last_name': user.last_name,
                                 'email': user.email,
                                 'full_name': f"{user.first_name} {user.last_name}",
                                 'token': token,
                                 })

        email_html = email_template.render(email_context)

        template = render_to_string("password_reset.html", context={
            'html_email': email_html,
            'subject': email.subject
        })
        text_content = strip_tags(template)

        email_text = EmailMultiAlternatives(
            email.subject,
            text_content,
            f'{email_config.title} <{email_config.email}>',
            [user.email]
        )
        email_text.attach_alternative(template, 'text/html')

        # connection.open()
        send_email(email_config, [email_text])

    return {"message": "success"}


def sendaccountactivationemail(user):
    app_config = AppConfig.objects.filter(app="main").first()
    if user is not None and app_config is not None:
        email = app_config.activate_account_email
        email_config = app_config.activate_account_emailconfig

        uid = urlsafe_base64_encode(force_bytes(user.pk)),
        token = account_activation_token.make_token(user),

        email_template = Template(email.body)
        email_context = Context({'first_name': user.first_name,
                                 'last_name': user.last_name,
                                 'email': user.email,
                                 'full_name': f"{user.first_name} {user.last_name}",
                                 'token': token[0],
                                 'uid': uid[0],
                                 })

        email_html = email_template.render(email_context)

        template = render_to_string("password_reset.html", context={
            'html_email': email_html,
            'subject': email.subject
        })
        text_content = strip_tags(template)

        email_text = EmailMultiAlternatives(
            email.subject,
            text_content,
            f'{email_config.title} <{email_config.email}>',
            [user.email]
        )
        email_text.attach_alternative(template, 'text/html')

        # connection.open()
        send_email(email_config, [email_text])

    return {"message": "success"}


def send_account_creation_email(user):
    app_config = AppConfig.objects.filter(app="main").first()
    if user is not None and app_config is not None:
        email = app_config.account_creation_email
        email_config = app_config.account_creation_emailconfig
        email_template = Template(email.body)
        email_context = Context({'first_name': user.first_name,
                                 'last_name': user.last_name,
                                 'email': user.email,
                                 'full_name': f"{user.first_name} {user.last_name}",
                                 })

        email_html = email_template.render(email_context)

        template = render_to_string("password_reset.html", context={
            'html_email': email_html,
            'subject': email.subject
        })
        text_content = strip_tags(template)

        email_text = EmailMultiAlternatives(
            email.subject,
            text_content,
            f'{email_config.title} <{email_config.email}>',
            [user.email]
        )
        email_text.attach_alternative(template, 'text/html')

        # connection.open()
        send_email(email_config, [email_text])

    return {"message": "success"}


def send_order_placement_email(order):
    app_config = AppConfig.objects.filter(app="main").first()
    ordera = Order.objects.get(id=order.id)

    order_ = OrderSerializer(ordera, many=False).data
    user = order.user
    if user is not None and app_config is not None:
        email = app_config.order_placement_email
        email_config = app_config.order_placement_emailconfig

        email_template = Template(email.body)
        email_context = Context({'first_name': user.first_name,
                                 'last_name': user.last_name,
                                 'email': user.email,
                                 'full_name': f"{user.first_name} {user.last_name}",
                                 'phone_number': user.profile.phone_number,
                                 'order': order,
                                 'items': order_['order_items'],
                                 'amount': order.amount,
                                 })

        email_html = email_template.render(email_context)

        template = render_to_string("password_reset.html", context={
            'html_email': email_html,
            'subject': email.subject
        })
        text_content = strip_tags(template)

        email_text = EmailMultiAlternatives(
            email.subject,
            text_content,
            f'{email_config.title} <{email_config.email}>',
            [user.email]
        )
        email_text.attach_alternative(template, 'text/html')

        # connection.open()
        send_email(email_config, [email_text])

    return {"message": "failed"}


def send_payment_received_email(order):
    app_config = AppConfig.objects.filter(app="main").first()
    ordera = Order.objects.get(id=order.id)

    order_ = OrderSerializer(ordera, many=False).data
    user = order.user
    if user is not None and app_config is not None:
        email = app_config.payment_made_email
        email_config = app_config.payment_made_emailconfig

        email_template = Template(email.body)
        email_context = Context({'first_name': user.first_name,
                                 'last_name': user.last_name,
                                 'email': user.email,
                                 'full_name': f"{user.first_name} {user.last_name}",
                                 'phone_number': user.profile.phone_number,
                                 'order': order,
                                 'items': order_['order_items'],
                                 'amount': order.amount,
                                 })

        email_html = email_template.render(email_context)

        template = render_to_string("password_reset.html", context={
            'html_email': email_html,
            'subject': email.subject
        })
        text_content = strip_tags(template)

        email_text = EmailMultiAlternatives(
            email.subject,
            text_content,
            f'{email_config.title} <{email_config.email}>',
            [user.email]
        )
        email_text.attach_alternative(template, 'text/html')

        # connection.open()
        send_email(email_config, [email_text])

    return {"message": "failed"}


def send_contact_us_email(contact_info):
    app_config = AppConfig.objects.filter(app="main").first()

    if app_config is not None:
        email = app_config.contact_email
        email_config = app_config.contact_emailconfig

        email_template = Template(email.body)
        email_context = Context({"contactInfo": contact_info})

        email_html = email_template.render(email_context)

        template = render_to_string("password_reset.html", context={
            'html_email': email_html,
            'subject': email.subject
        })
        text_content = strip_tags(template)

        email_text = EmailMultiAlternatives(
            email.subject,
            text_content,
            f'{email_config.title} <{email_config.email}>',
            ['rovinewanjala99@gmail.com']
        )
        email_text.attach_alternative(template, 'text/html')

        email_text_2 = EmailMultiAlternatives(
            email.subject,
            text_content,
            f'{email_config.title} <{email_config.email}>',
            ['info@gizpassion.com']
        )
        email_text_2.attach_alternative(template, 'text/html')

        # connection.open()
        send_email(email_config, [email_text, email_text_2])

    return {"message": "success"}


def send_subscription_confirmation_email(subscriber):
    app_config = AppConfig.objects.filter(app="main").first()

    if app_config is not None:
        email = app_config.subscription_confirmation_email
        email_config = app_config.subscription_confirmation_emailconfig

        email_template = Template(email.body)
        email_context = Context({'subscriber': subscriber})

        email_html = email_template.render(email_context)

        template = render_to_string("password_reset.html", context={
            'html_email': email_html,
            'subject': email.subject
        })
        text_content = strip_tags(template)

        email_text = EmailMultiAlternatives(
            email.subject,
            text_content,
            f'{email_config.title} <{email_config.email}>',
            [subscriber.email]
        )
        email_text.attach_alternative(template, 'text/html')

        # connection.open()
        send_email(email_config, [email_text])

    return {"message": "success"}


def send_company_creation_email(company):
    app_config = AppConfig.objects.filter(app="main").first()

    if app_config is not None:
        email = app_config.company_creation_email
        email_config = app_config.company_creation_emailconfig

        email_template = Template(email.body)
        email_context = Context({'company': company})

        email_html = email_template.render(email_context)

        template = render_to_string("password_reset.html", context={
            'html_email': email_html,
            'subject': email.subject
        })
        text_content = strip_tags(template)

        email_text = EmailMultiAlternatives(
            email.subject,
            text_content,
            f'{email_config.title} <{email_config.email}>',
            [settings.ADMIN_EMAILS]
        )
        email_text.attach_alternative(template, 'text/html')

        # connection.open()
        send_email(email_config, [email_text])

    return {"message": "success"}


class EmailViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows emails to be viewed or edited.
    """
    queryset = Email.objects.all()
    serializer_class = EmailSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    pagination_class = StandardResultsSetPagination

    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['created_by__id']
    search_fields = ["subject", "body", "description"]


class EmailConfigViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows email configurations to be viewed or edited.
    """
    queryset = EmailConfiguration.objects.all()
    serializer_class = EmailConfigSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    pagination_class = StandardResultsSetPagination

    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['created_by__id']
    search_fields = ["title", "email"]
