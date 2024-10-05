from rest_framework import serializers
from . models import Component, Vehicle, VehicleIssue

class ComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Component
        fields = '__all__'


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = '__all__'


class VehicleIssueSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = VehicleIssue
        fields = '__all__'

    def get_total_price(self, obj):
        return obj.calculate_total_price()