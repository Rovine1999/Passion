from rest_framework import routers
from django.urls import path, include
from .endpoints import ChatMessagesViewSet, GroupChatMessagesViewSet

from .views import *

router = routers.DefaultRouter()
router.register('messages/chat-group',
                ChatMessagesViewSet)  # These are private messages between farmers and other users of the system
router.register('messages/groups', GroupChatMessagesViewSet)  # These are farmer group messages

urlpatterns = [
    path('', interact, name='interact'),
    path('post/<str:post_id>/<str:slug>/', single_post, name="post"),
    path('api/add-friend/', add_friend, name='add-friend0'),
    path('api/', include(router.urls))
]
