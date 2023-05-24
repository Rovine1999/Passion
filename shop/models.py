from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

import random
import string


def generate_uuid():
    """
    Generate a random UUID consisting of 5 uppercase letters and numbers.
    """
    characters = string.ascii_uppercase + string.digits
    uuid = ''.join(random.choice(characters) for _ in range(6))
    return uuid


# Create your models here
PRODUCT_CHOICES = (
    ('product', 'Product'),
    ('input', 'Input'),
    ('sweet_passion', 'Sweet Passion'),
    ('other_fruit', 'Other Fruit')
)

FERTILIZER_CHOICES = (
    ('can', 'CAN'),
    ('dap', 'DAP'),
    ('npk', 'NPK'),
)

SEEDLING_CHOICES = (
    ('kp4', 'KP4'),
)

CATEGORY_CHOICES = (
    ('fertilizer', 'Fertilizer'),
    ('seedling', 'Seedlings'),
)

QUALITY_CHOICES = (
    ('grade1', 'Grade 1'),
    ('grade2', 'Grade 2'),
    ('grade3', 'Grade 3'),

)


class Category(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)
    featured = models.BooleanField(default=False)
    order = models.IntegerField(blank=True, null=True)
    image = models.FileField(
        upload_to='categories/images/', blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super(Category, self).save(*args, **kwargs)


class Product(models.Model):
    created_by = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=100, blank=False, null=False)
    description = models.TextField()
    category = models.ForeignKey(
        Category, blank=True, null=True, on_delete=models.SET_NULL)
    available = models.BooleanField(default=True)
    price = models.FloatField()
    discount = models.DecimalField(
        blank=True, null=True, max_digits=3, decimal_places=2)
    county = models.ForeignKey(
        'mainapp.County', blank=True, null=True, on_delete=models.SET_NULL)
    image = models.ImageField(
        upload_to='products/images/', blank=False, null=False)
    product_type = models.CharField(
        max_length=30, choices=PRODUCT_CHOICES, blank=True, null=True)
    featured = models.BooleanField(default=False)

    created_on = models.DateTimeField(auto_created=True, auto_now_add=True)
    updated_on = models.DateTimeField(auto_created=True, auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # self.created_by = self.request.user
        return super(Product, self).save(*args, **kwargs)


class Buy(models.Model):
    user = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.CASCADE)
    phone_number = models.CharField(blank=False, null=False, max_length=9)
    product_name = models.CharField(max_length=150, blank=True, null=True)
    category = models.CharField(
        max_length=30, choices=CATEGORY_CHOICES, blank=True, null=True)
    seedling_type = models.CharField(
        max_length=30, choices=SEEDLING_CHOICES, blank=True, null=True)
    fertilizer_type = models.CharField(
        max_length=30, choices=FERTILIZER_CHOICES, blank=True, null=True)
    metric = models.FloatField(max_length=10, blank=True, null=True)

    created_on = models.DateTimeField(auto_created=True, auto_now_add=True)
    updated_on = models.DateTimeField(auto_created=True, auto_now=True)

    def save(self, *args, **kwargs):
        self.user = User.objects.filter(
            profile__phone_number=self.phone_number).first()
        return super(Buy, self).save(*args, **kwargs)


class Sell(models.Model):
    user = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.CASCADE)
    phone_number = models.CharField(blank=False, null=False, max_length=9)
    grade = models.CharField(
        max_length=30, choices=QUALITY_CHOICES, blank=True, null=True)
    metric = models.FloatField(max_length=10, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.user = User.objects.filter(
            profile__phone_number=self.phone_number).first()
        return super(Sell, self).save(*args, **kwargs)


class Order(models.Model):
    user = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.SET_NULL)
    uuid = models.CharField(max_length=10, blank=True, null=True)
    paid = models.BooleanField(default=False)
    amount = models.FloatField()

    created_on = models.DateTimeField(auto_created=True, auto_now_add=True)
    updated_on = models.DateTimeField(auto_created=True, auto_now=True)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        if not self.pk:
            # Generate a new UUID for a new instance of the model
            while True:
                uuid = generate_uuid()
                if not Order.objects.filter(uuid=uuid).exists():
                    self.uuid = uuid
                    break

        super().save(*args, **kwargs)


class OrderItem(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True, blank=False)
    price = models.FloatField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE,
                              null=True, blank=False, related_name='order_items')
    quantity = models.IntegerField(default=0)

    created_on = models.DateTimeField(auto_created=True, auto_now_add=True)
    updated_on = models.DateTimeField(auto_created=True, auto_now=True)

    def __str__(self):
        return f"Order - {self.order.id}"


class Cart(models.Model):
    user = models.OneToOneField(
        User, blank=True, null=True, on_delete=models.SET_NULL)
    paid = models.BooleanField(default=False)
    amount = models.FloatField()

    created_on = models.DateTimeField(auto_created=True, auto_now_add=True)
    updated_on = models.DateTimeField(auto_created=True, auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Cart"


class CartItem(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True, blank=False)
    price = models.FloatField()
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE,
                             null=True, blank=False, related_name='cart_items')
    quantity = models.IntegerField(default=0)

    created_on = models.DateTimeField(auto_created=True, auto_now_add=True)
    updated_on = models.DateTimeField(auto_created=True, auto_now=True)

    def __str__(self):
        return f"Cart - {self.cart.id}"

    def save(self, *args, **kwargs):
        self.price = self.product.price
        return super(CartItem, self).save(*args, **kwargs)


class Payment(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, null=True, blank=False, related_name='payment')
    amount = models.FloatField()
    transaction_date = models.CharField(max_length=55, blank=True, null=True)
    transaction_code = models.CharField(max_length=30, blank=True, null=True)

    created_on = models.DateTimeField(auto_created=True, auto_now_add=True)
    updated_on = models.DateTimeField(auto_created=True, auto_now=True)

    def __str__(self):
        return f"Order - {self.order.id}"
