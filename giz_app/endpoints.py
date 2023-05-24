from rest_framework import viewsets
from django.contrib.auth.models import User
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from shop.models import Order, Buy, Sell
from shop.serializers import OrderSerializer, BuySerializer, SellSerializer
from .models import Profile, Farmer, Processors, Enumerator, Aggregator
from .serializers import ProfileSerializer, UserSerializer, FarmerSerializer, ServiceProviderSerializer, \
    EnumeratorSerializer, AggregatorSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.get_queryset()
    serializer_class = ProfileSerializer

    # filter_backends = [DjangoFilterBackend, SearchFilter]
    # search_fields = ['username', 'user_profile__phone_number']


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.get_queryset()
    serializer_class = UserSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['username', 'user_profile__phone_number']


class FarmersViewSet(viewsets.ModelViewSet):
    queryset = Farmer.objects.get_queryset()
    serializer_class = FarmerSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['user__username', 'user__profile__phone_number',
                     'user__profile__phone_number', 'farmer_number']


class EnumeratorViewSet(viewsets.ModelViewSet):

    queryset = Enumerator.objects.get_queryset()
    serializer_class = EnumeratorSerializer


class AggregatorViewSet(viewsets.ModelViewSet):

    queryset = Aggregator.objects.get_queryset()
    serializer_class = AggregatorSerializer


class ProcessorsViewSet(viewsets.ModelViewSet):

    queryset = Processors.objects.get_queryset()
    serializer_class = ServiceProviderSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['user__username', 'company_name', 'description']


class OrderViewSet(viewsets.ModelViewSet):

    queryset = Order.objects.get_queryset()
    serializer_class = OrderSerializer


class BuyViewSet(viewsets.ModelViewSet):

    queryset = Buy.objects.get_queryset()
    serializer_class = BuySerializer


class SellViewSet(viewsets.ModelViewSet):

    queryset = Sell.objects.get_queryset()
    serializer_class = SellSerializer
