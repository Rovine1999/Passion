import json

from django.shortcuts import redirect
import requests

from mainapp.models import AppConfig
from .models import *
from giz_app.models import County
from rest_framework.response import Response
from django.contrib import messages
from rest_framework.decorators import api_view

from mailer.views import send_order_placement_email, send_payment_received_email

from django.conf import settings
from django.urls import reverse
from django.db.models import Q

import logging

from coinbase_commerce.client import Client
from coinbase_commerce.error import SignatureVerificationError, WebhookInvalidPayload
from coinbase_commerce.webhook import Webhook
from giz_app.models import CollectionCenter

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .decorators import attach_categories_to_request, attach_featured_products, attach_new_products
from django.core.paginator import Paginator


@attach_categories_to_request
@attach_featured_products
@attach_new_products
def marketplace(request):
    farmers_ = Product.objects.all()
    paginator = Paginator(farmers_, 25)  # Show 25 farmers per page.

    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    products_context = {
        "page_obj": page_obj,
        "pages": paginator.page_range,
        "page_count": paginator.num_pages,
        "products_total": paginator.count,
    }

    featured_categories = Category.objects.filter(featured=True).order_by('order')
    categories_data = []
    for cat in featured_categories:
        category = {
            "name": cat.name,
            "id": cat.id,
            "slug": cat.slug,
            "products": Product.objects.filter(category=cat)[0:6]
        }
        categories_data.append(category)
    context = {
        "counties": County.objects.all(),
        "categories": categories_data,
        "collectioncenters": CollectionCenter.objects.filter(flashsale=True),
        **products_context,
    }
    return render(request, template_name='agrul/pages/market/shop.html', context=context)


@attach_categories_to_request
def new_products(request):
    context = {
        "products": Product.objects.all().order_by("-id")
    }
    return render(request, template_name='market/pages/new-products.html', context=context)


@attach_categories_to_request
def featured_products(request):
    context = {
        "products": Product.objects.filter(featured=True).order_by("-id")
    }
    return render(request, template_name='market/pages/featured-products.html', context=context)


@attach_categories_to_request
def search_products(request):
    query = request.GET.get('q')

    if query:
        products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query) |
                                          Q(product_type__icontains=query))
    else:
        products = []

    context = {
        'query': query,
        'products': products,
    }
    return render(request, template_name='market/pages/search-products.html', context=context)


@attach_categories_to_request
def single_category(request, category_id, category_slug):
    county = request.GET.get('county', 'all')
    if category_id == 'all':
        products = Product.objects.all().order_by("-id") if county == 'all' else Product.objects.filter(
            county__id=county)
        context = {
            "products": products,
            "category": {
                "name": 'All Products',
            },
        }
    else:
        category = Category.objects.filter(id=category_id).first()
        products_per_category = Product.objects.filter(category=category).order_by("-id")
        products = products_per_category if county == 'all' else products_per_category.filter(county__id=county)
        context = {
            "products": products,
            "category": category,
        }
    return render(request, template_name='market/pages/single-category.html', context=context)


@attach_categories_to_request
def single_county(request, county_id, county_slug):
    county = County.objects.filter(id=county_id).first()
    context = {
        'products': Product.objects.filter(product_type='product').filter(county=county),
        'inputs': Product.objects.filter(product_type='input').filter(county=county),
        'other_fruits': Product.objects.filter(product_type='other_fruit').filter(county=county),
        'sweet_passions': Product.objects.filter(product_type='sweet_passion').filter(county=county),
        'counties': County.objects.all(),
        'county': county,
    }
    return render(request, template_name='marketplace/marketplace.html', context=context)


def checkout(request):
    return render(request, template_name='agrul/pages/market/checkout.html', context={})


@api_view(['POST'])
def place_order(request):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        data = request.data

        items = json.loads(data.get('data'))
        phone_number = data.get('phone_number')

        total = 0
        order_items = []
        for item in items:
            product = Product.objects.filter(id=item['id']).first()
            if product is not None:
                total += product.price * item["qty"]
                order_items.append(
                    OrderItem(product=product, price=product.price, quantity=item["qty"]))
        order = Order.objects.create(user=request.user, amount=total)
        order.save()
        for order_item in order_items:
            order_item.order = order

        OrderItem.objects.bulk_create(order_items)

        send_order_placement_email(order)
        MpesaSTKPushPost(order.id, order.amount, phone_number)
        return Response({"message": "success", "order": "created"})
    messages.error(request, "An error occurred while placing the order")
    return redirect('checkout')


@api_view(['POST'])
def make_payment(request):
    return Response({"m": "message"})


def single_order(request, order_id):
    order = Order.objects.filter(id=order_id).first()
    items = OrderItem.objects.filter(order=order)
    appconfig = AppConfig.objects.get(app="main")
    client = Client(api_key=settings.COINBASE_COMMERCE_API_KEY)
    product = {
        'name': f"Order#{order.id}",
        'description': f"You are making payment for the order you made earlier. The total amount is KES {order.amount} "
                       f"which is approximately ${order.amount / 120}. The total products ordered were - {len(items)}",
        'local_price': {
            'amount': f"{order.amount / 120}",
            'currency': 'USD'
        },
        'metadata': {
            'order_id': order.id
        },
        'pricing_type': 'fixed_price',
        'redirect_url': f"{appconfig.application_url}{reverse('single_order_success', args=[order.id])}",
        'cancel_url': f"{appconfig.application_url}{reverse('single_order_failed', args=[order.id])}",
    }
    charge = client.charge.create(**product)

    return render(request, 'agrul/pages/account/single-order.html', {
        'charge': charge,
        'order': order,
        'items': items,
    })


def single_order_success(request, order_id):
    order = Order.objects.filter(id=order_id).first()
    return render(request, 'account/payments/success.html', {
        'order': order,
    })


def single_order_failed(request, order_id):
    order = Order.objects.filter(id=order_id).first()
    return render(request, 'account/payments/failed.html', {
        'order': order,
    })


@csrf_exempt
@require_http_methods(['POST'])
def coinbase_webhook(request):
    logger = logging.getLogger(__name__)

    request_data = request.body.decode('utf-8')
    request_sig = request.headers.get('X-CC-Webhook-Signature', None)
    webhook_secret = settings.COINBASE_COMMERCE_WEBHOOK_SHARED_SECRET

    try:
        event = Webhook.construct_event(
            request_data, request_sig, webhook_secret)

        # List of all Coinbase webhook events:
        # https://commerce.coinbase.com/docs/api/#webhooks
        # Coinbase Wallet supports all ERC-20 tokens as well as Bitcoin, Dogecoin and Litecoin. 
        # Coinbase Wallet says it supports thousands of digital assets, including NFTs. 
        # It also has features that include purchases, swaps and staking directly from the wallet.

        if event['type'] == 'charge:confirmed':
            logger.info('Payment confirmed.')
            order_id = event['data']['metadata']['order_id']
            order = Order.objects.filter(id=order_id).first()
            if order is not None:
                order.paid = True
                order.save()
                send_payment_received_email(order)

    except (SignatureVerificationError, WebhookInvalidPayload) as e:
        return HttpResponse(e, status=400)

    logger.info(f'Received event: id={event.id}, type={event.type}')
    return HttpResponse('ok', status=200)


@csrf_exempt
@api_view(['POST'])
def mpesa_payment_webhook(request):
    data = request.data
    transaction_date = data["date"]
    amount = data["amount"]
    transaction_code = data["transaction_code"]
    order_id = data["order_id"]  # or UUID

    order = Order.objects.filter(Q(id=order_id) | Q(uuid=order_id)).first()
    if order:
        order.paid = True
        order.save()
        send_payment_received_email(order)
        payment = Payment.objects.create(
            order=order,
            transaction_code=transaction_code,
            amount=amount,
            transaction_date=transaction_date
        )
        payment.save()
        return Response({
            "message": "Payment successful"
        })
    else:
        return Response({
            "message": "Payment failed. Order not found"
        })


def MpesaSTKPushPost(order_id_, amount_, phone_number_):
    url = 'https://e4impact.e-granary.com/api/ipn/ke/mpesa/lnmo/transact'
    data = {
        "order_id": order_id_,
        "amount": amount_,
        "phone_number": phone_number_
    }
    response = requests.post(url, data=data)
    return response
