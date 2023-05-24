from rest_framework import serializers
from .models import Product, OrderItem, Cart, CartItem, Order, Payment, Sell, Buy
from giz_app.pubserializers import UserSerializer


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'name', 'price']


class OrderItemSerializer(serializers.ModelSerializer):
    total = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ['id', 'price', 'product', 'total', 'quantity']

    def get_total(self, obj):
        return obj.price * obj.quantity

    def to_representation(self, instance):
        self.fields["product"] = ProductSerializer(many=False)
        return super(OrderItemSerializer, self).to_representation(instance)


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ['id', 'user', 'uuid', 'amount',
                  'order_items', 'paid', 'payment']

    def to_representation(self, instance):
        self.fields["order_items"] = OrderItemSerializer(many=True)
        self.fields["payment"] = PaymentSerializer(many=True)
        self.fields["user"] = UserSerializer(many=False)
        return super(OrderSerializer, self).to_representation(instance)


class CartItemSerializer(serializers.ModelSerializer):
    total = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'price', 'product', 'total', 'quantity']

    def get_total(self, obj):
        return obj.product.price * obj.quantity

    def to_representation(self, instance):
        self.fields["product"] = ProductSerializer(many=False)
        return super(CartItemSerializer, self).to_representation(instance)


class CartSerializer(serializers.ModelSerializer):
    total_amount = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'total_amount', 'cart_items']

    def to_representation(self, instance):
        self.fields["cart_items"] = CartItemSerializer(many=True)
        return super(CartSerializer, self).to_representation(instance)

    def get_total_amount(self, obj):
        total = 0
        for item in obj.cart_items:
            item_total = item.price * item.quantity
            total += item_total

        return total


class SellSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sell
        fields = ['id', 'phone_number', 'grade', 'metric']


class BuySerializer(serializers.ModelSerializer):

    class Meta:
        model = Buy
        fields = ['id',  'phone_number', 'product_name',
                  'category', 'seedling_type', 'fertilizer_type', 'metric']
