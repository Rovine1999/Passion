from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    profile_info = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "first_name", "email", "last_name", "username", "password", "profile", "profile_info"]
        extra_kwargs = {
            "password": {
                "write_only": True
            }
        }

    def to_representation(self, instance):
        return super(UserSerializer, self).to_representation(instance)

    def profile_photo(self, obj):
        request = self.context.get('request')
        if bool(obj.profile.profile_photo) is True:
            photo_url = obj.profile.profile_photo.url
            # return request.build_absolute_url(photo_url)
            return photo_url
        return None

    def get_profile_info(self, obj):
        request = self.context.get('request')
        return {
            "phone_number": obj.profile.phone_number,
            "profile_photo": self.profile_photo(obj)
        }
