from giz_app.serializers import FarmerSerializer
from resources.models import DemoFarm, County, Nursery, FarmerGroup

from rest_framework import serializers


class CountySerializer(serializers.ModelSerializer):

    class Meta:
        model = County
        fields = '__all__'


class DemoFarmSerializer(serializers.ModelSerializer):

    class Meta:
        model = DemoFarm
        fields = '__all__'

    def to_representation(self, instance):
        self.fields["county"] = CountySerializer(many=False)
        return super(DemoFarmSerializer, self).to_representation(instance)


class NurserySerializer(serializers.ModelSerializer):

    class Meta:
        model = Nursery
        fields = '__all__'

    def to_representation(self, instance):
        self.fields["county"] = CountySerializer(many=False)
        return super(NurserySerializer, self).to_representation(instance)


class FarmerGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = FarmerGroup
        fields = ['id', 'code', 'county_number', 'county', 'title', 'description', 'location', 'image']

    def to_representation(self, instance):
        self.fields["county"] = CountySerializer(many=False)
        # self.fields['farmers'] = FarmerSerializer(many=True)
        return super(FarmerGroupSerializer, self).to_representation(instance)
