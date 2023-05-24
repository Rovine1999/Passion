from rest_framework import routers
from django.urls import path, include
from .endpoints import ProfileViewSet, UsersViewSet, FarmersViewSet, ProcessorsViewSet, OrderViewSet, BuyViewSet, SellViewSet, \
    EnumeratorViewSet, AggregatorViewSet

router = routers.DefaultRouter()
router.register(r'users', UsersViewSet)
router.register(r'user-profiles', ProfileViewSet)
router.register(r'farmers', FarmersViewSet)
router.register(r'enumerators', EnumeratorViewSet)
router.register(r'aggregators', AggregatorViewSet)
router.register(r'processors', ProcessorsViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'buy', BuyViewSet)
router.register(r'sell', SellViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
