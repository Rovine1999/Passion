from .views import *
from django.urls import path

urlpatterns = [
    path('', marketplace, name='marketplace'),
    path('search/', search_products, name="search_products"),
    path('products/new/', new_products, name='new_products'),
    path('products/featured/', featured_products, name='featured_products'),
    path('category/<str:category_id>/<str:category_slug>/products/', single_category, name='category'),

    path('checkout', checkout, name="checkout"),
    path('checkout/orders/make/', place_order, name="place_order"),

    path('checkout/orders/webhook/', coinbase_webhook, name="web_hook"),
    path('checkout/orders/mpesa-webhook/', mpesa_payment_webhook, name="mpesa_web_hook"),

    path('checkout/orders/single/<str:order_id>/', single_order, name="single_order"),
    path('checkout/orders/single/<str:order_id>/success/', single_order_success, name="single_order_success"),
    path('checkout/orders/single/<str:order_id>/failed/', single_order_failed, name="single_order_failed"),

    path('counties/<str:county_id>/<str:county_slug>/', single_county, name='single_county'),
]
