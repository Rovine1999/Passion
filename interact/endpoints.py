from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import *


class UserChatGroupViewSet(viewsets.ModelViewSet):
    queryset = UserChatGroup.objects.get_queryset().order_by('id')
    serializer_class = UserChatGroupSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # search_fields = []
    filterset_fields = ['id', 'chat_name']


class ChatMessagesViewSet(viewsets.ModelViewSet):
    queryset = ChatMessage.objects.get_queryset().select_related('sender').order_by('id')
    serializer_class = ChatMessageSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # search_fields = []
    filterset_fields = ['id', 'chat_group__chat_name']


class GroupChatMessagesViewSet(viewsets.ModelViewSet):
    queryset = GroupChatMessage.objects.get_queryset().select_related('sender').order_by('id')
    serializer_class = GroupChatMessageSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # search_fields = []
    filterset_fields = ['id', 'group__id']

