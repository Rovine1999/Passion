from django.contrib import messages
from django.shortcuts import redirect
from .models import Category, Product


def attach_categories_to_request(view_func):
    def wrapper_func(request, *args, **kwargs):
        request.categories = Category.objects.all()
        return view_func(request, *args, **kwargs)

    return wrapper_func


def attach_featured_products(view_func):
    def wrapper_func(request, *args, **kwargs):
        request.featured_products = Product.objects.filter(featured=True)
        return view_func(request, *args, **kwargs)

    return wrapper_func


def attach_new_products(view_func):
    def wrapper_func(request, *args, **kwargs):
        request.new_products = Product.objects.all().order_by('-id')[0: 10]
        return view_func(request, *args, **kwargs)

    return wrapper_func

