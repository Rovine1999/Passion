from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, Farmer, Processors, Enumerator, CollectionCenter, Aggregator, TransportLogistics, \
    InputSuppliersAndAgrovets, FinancialProvider, InsuranceProvider, CountyGovernment, Coperatives, Company
from django.contrib.auth.hashers import make_password

from drf_writable_nested import WritableNestedModelSerializer


class ProfileSerializer(serializers.ModelSerializer):
    # profile_photo = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ["phone_number", "alt_phone_number", "year_of_birth", "gender", "county", "profile_photo"]

        extra_kwargs = {
            "profile_photo": {
                "required": False
            },
            "alt_phone_number": {
                "required": False
            }
        }

    def get_profile_photo(self, obj):
        request = self.context.get('request')
        if bool(obj.profile_photo) is True:
            photo_url = obj.profile_photo.url
            # return request.build_absolute_url(photo_url)
            return photo_url
        return None


class UserSerializer(WritableNestedModelSerializer):
    profile = ProfileSerializer(required=False)

    class Meta:
        model = User
        fields = ["id", "password", "email", "first_name", "last_name", "username", "profile"]
        extra_kwargs = {
            "email": {
                "required": False
            },
            "password": {
                "write_only": True,
                "required": False
            },
            "username": {
                "required": False,
            }
        }

    def to_representation(self, instance):
        self.fields['profile'] = ProfileSerializer(many=False)
        return super(UserSerializer, self).to_representation(instance)

    def create(self, validated_data, *args, **kwargs):
        validated_data['password'] = make_password(validated_data.get('password', validated_data.get('username')))
        return super().create(validated_data, *args, **kwargs)

    def update(self, instance, validated_data):
        for key in list(validated_data.keys()):
            if key not in self.initial_data:
                validated_data.pop(key)
        return super().update(instance, validated_data)


class FarmerSerializer(WritableNestedModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Farmer
        fields = ["id", "user", "county", "county_name", "sub_county", "county_number",  "acreage",
                  "enumerator_code", "enumerator", "selling_place", "farmer_group_code",
                  "farmer_number", "landmark"]

        extra_kwargs = {
            "county": {
                "required": False
            },
            "enumerator": {
                "required": False
            }
        }

    def to_representation(self, instance):
        self.fields['user'] = UserSerializer(many=False)
        return super(FarmerSerializer, self).to_representation(instance)


class AggregatorSerializer(WritableNestedModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Aggregator
        fields = ["id", "user", "code", "name", "county", "county_number", "mobile_number", "location"]

        extra_kwargs = {
            "county": {
                "required": False,
            },
            "code": {
                "read_only": True
            },
        }

    def to_representation(self, instance):
        self.fields['user'] = UserSerializer(many=False)
        return super(AggregatorSerializer, self).to_representation(instance)


class CompanySerializer(WritableNestedModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Company
        fields = ["id", "user", "name", "code"]

        # extra_kwargs = {
        #     "county": {
        #         "required": False
        #     }
        # }

    def to_representation(self, instance):
        self.fields['user'] = UserSerializer(many=False)
        return super(CompanySerializer, self).to_representation(instance)


class EnumeratorSerializer(WritableNestedModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Enumerator
        fields = ["id", "user", "county", "code", "county_number", "company", "phone_number"]

        extra_kwargs = {
            "county": {
                "required": False
            },
            "phone_number": {
              "required": False
            },
            "code": {
                "read_only": True
            },
        }

    def to_representation(self, instance):
        self.fields['user'] = UserSerializer(many=False)
        self.fields['company'] = CompanySerializer(many=False)
        return super(EnumeratorSerializer, self).to_representation(instance)


class ServiceProviderSerializer(WritableNestedModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Processors
        fields = ['id', 'user', 'location', 'company_name', 'image', 'description']

    def to_representation(self, instance):
        return super(ServiceProviderSerializer, self).to_representation(instance)


class CollectionCenterSerializer(serializers.ModelSerializer):

    class Meta:
        model = CollectionCenter
        fields = '__all__'

        depth = 3


class AbstractServiceProviderSerializer(WritableNestedModelSerializer):
    user = UserSerializer()

    class Meta:
        fields = ['id', 'user', 'location', 'company_name', 'code', 'county', 'sub_county', 'county_number', 'image',
                  'description', 'contact_person_name', 'phone_number_contact_person']
        abstract = True


class ProcessorSerializer(AbstractServiceProviderSerializer):
    class Meta:
        model = Processors
        fields = '__all__'

    def to_representation(self, instance):
        return super(ProcessorSerializer, self).to_representation(instance)


class TransportLogisticSerializer(AbstractServiceProviderSerializer):
    class Meta:
        model = TransportLogistics
        fields = '__all__'

    def to_representation(self, instance):
        return super(TransportLogisticSerializer, self).to_representation(instance)


class InputSuppliersAndAgrovetsSerializer(AbstractServiceProviderSerializer):
    class Meta:
        model = InputSuppliersAndAgrovets
        fields = '__all__'

    def to_representation(self, instance):
        return super(InputSuppliersAndAgrovetsSerializer, self).to_representation(instance)


class FinancialProviderSerializer(AbstractServiceProviderSerializer):
    class Meta:
        model = FinancialProvider
        fields = '__all__'

    def to_representation(self, instance):
        return super(FinancialProviderSerializer, self).to_representation(instance)


class InsuranceProviderSerializer(AbstractServiceProviderSerializer):
    class Meta:
        model = InsuranceProvider
        fields = '__all__'

    def to_representation(self, instance):
        return super(InsuranceProviderSerializer, self).to_representation(instance)


class CountyGovernmentSerializer(AbstractServiceProviderSerializer):
    class Meta:
        model = CountyGovernment
        fields = '__all__'

    def to_representation(self, instance):
        return super(CountyGovernmentSerializer, self).to_representation(instance)


class CoperativesSerializer(AbstractServiceProviderSerializer):
    class Meta:
        model = Coperatives
        fields = '__all__'

    def to_representation(self, instance):
        return super(CoperativesSerializer, self).to_representation(instance)

