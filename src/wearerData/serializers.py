
from rest_framework import serializers, exceptions
from .models import WearerData, WearerEvent, WearerLocation, WearerMeter

from django.utils.translation import ugettext_lazy as _


class WearerDataSerializer(serializers.Serializer):
    nowTime = serializers.TimeField(read_only=True)
    nowDate = serializers.DateField(read_only=True)
    temp = serializers.CharField(max_length=50)
    humid = serializers.CharField(max_length=50)

    heartRate = serializers.CharField(max_length=50)

    # override

    def create(self, validated_data):
        """
        Create and return a new LinkedUser instance, given the validated data.
        """
        # wearer = CustomUser.objects.get(username=self.user_id)
        return WearerData.objects.create(**validated_data)


class WearerLocationSerializer(serializers.Serializer):
    nowDT = serializers.DateTimeField(read_only=True)
    latitude = serializers.CharField(max_length=50)
    longitude = serializers.CharField(max_length=50)

    def create(self, validated_data):
        return WearerLocation.objects.create(**validated_data)


class WearerMeterSerializer(serializers.Serializer):
    nowDT = serializers.DateTimeField(read_only=True)
    meter = serializers.CharField(max_length=50)

    def validate_meter(self, value):
        try:
            val = int(value)
            return val
        except:
            raise(ValueError("meter value should be written in int"))

    def create(self, validated_data):
        return WearerMeter.objects.create(**validated_data)


class WearerEventSerializer(serializers.Serializer):
    nowDate = serializers.DateField(read_only=True)
    nowTime = serializers.TimeField(read_only=True)
    fallEvent = serializers.CharField(max_length=1)
    heartEvent = serializers.CharField(max_length=1)
    heatIllEvent = serializers.CharField(max_length=1)

    def validate_fallEvent(self, value):
        if value.upper() == "T":
            return True
        elif value.upper() == "F":
            return False

        else:
            raise serializers.ValidationError(
                _('fallEvent value should be T,t or F,f'))

    def validate_heartEvent(self, value):
        if value.upper() == "T":
            return True
        elif value.upper() == "F":
            return False

        else:
            raise serializers.ValidationError(
                _('heartRate value should be T,t or F,f'))

    def validate_heatIllEvent(self, value):
        return "N"

    def create(self, validated_data):
        return WearerEvent.objects.create(**validated_data)
