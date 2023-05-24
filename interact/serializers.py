from rest_framework import serializers

from giz_app.pubserializers import UserSerializer
from resources.serializers import FarmerGroupSerializer
from .models import UserChatGroup, ChatMessage, ChatFile, GroupChatMessage


class UserChatGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserChatGroup
        fields = ['id', 'user_1', 'user_2', 'chat_name', 'created_on']

    def to_representation(self, instance):
        # self.fields['user_1'] = UserSerializer(many=False)
        # self.fields['user_2'] = UserSerializer(many=False)
        return super(UserChatGroupSerializer, self).to_representation(instance)


class ChatFileSerializer(serializers.ModelSerializer):

    class Meta:
        model = ChatFile
        fields = '__all__'


class ChatMessageSerializer(serializers.ModelSerializer):
    created_on = serializers.SerializerMethodField()

    class Meta:
        model = ChatMessage
        fields = ['id', 'chat_group', 'sender', 'text', 'files', 'created_on']

        extra_kwargs = {
            "files": {
                "required": False
            }
        }

    def to_representation(self, instance):
        self.fields['sender'] = UserSerializer(many=False)
        self.fields['files'] = ChatFileSerializer(many=True)
        self.fields['chat_group'] = UserChatGroupSerializer(many=False)
        return super(ChatMessageSerializer, self).to_representation(instance)

    def get_created_on(self, obj):
        return obj.created_on.strftime("%b %Y %d | %I:%M%p")

    def create(self, validated_data, *args, **kwargs):
        files = self.initial_data.getlist('files_')

        files_arr = []
        if len(files) > 0 and files:
            for file_ in files:
                if not isinstance(file_, str):
                    file__ = ChatFile.objects.create(file=file_, file_type=file_.content_type)
                    files_arr.append(file__)
        files_ = [file.id for file in files_arr]
        validated_data['files'] = files_

        return super().create(validated_data, *args, **kwargs)


class GroupChatMessageSerializer(serializers.ModelSerializer):
    created_on = serializers.SerializerMethodField()

    class Meta:
        model = GroupChatMessage
        fields = ['id', 'group', 'sender', 'text', 'files', 'created_on']

        extra_kwargs = {
            "files": {
                "required": False
            }
        }

    def to_representation(self, instance):
        self.fields['sender'] = UserSerializer(many=False)
        self.fields['files'] = ChatFileSerializer(many=True)
        self.fields['group'] = FarmerGroupSerializer(many=False)
        return super(GroupChatMessageSerializer, self).to_representation(instance)

    def get_created_on(self, obj):
        return obj.created_on.strftime("%b %Y %d | %I:%M%p")

    def create(self, validated_data, *args, **kwargs):
        files = self.initial_data.getlist('files_')

        files_arr = []
        if len(files) > 0 and files:
            for file_ in files:
                if not isinstance(file_, str):
                    file__ = ChatFile.objects.create(file=file_, file_type=file_.content_type)
                    files_arr.append(file__)
        files_ = [file.id for file in files_arr]
        validated_data['files'] = files_

        return super().create(validated_data, *args, **kwargs)
