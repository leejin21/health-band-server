
from rest_framework import serializers, exceptions
from .models import WearerData, WearerEvent

from django.utils.translation import ugettext_lazy as _


# TODO serializers 채우기
# TODO login한 상태에서 self.user로 굳이 serializer에서 명시하지 않아도 되는 지.(이 경우 view에서 그냥 추가해 주면 되는 건 지)

class WearerDataSerializer(serializers.Serializer):
    nowTime = serializers.TimeField(read_only=True)
    nowDate = serializers.DateField(read_only=True)
    temp = serializers.CharField(max_length=50)
    humid = serializers.CharField(max_length=50)

    heartRate = serializers.CharField(max_length=50)
    sound = serializers.CharField(max_length=50)
    stepCount = serializers.CharField(max_length=50)

    # override

    def create(self, validated_data):
        """
        Create and return a new LinkedUser instance, given the validated data.
        """
        # wearer = CustomUser.objects.get(username=self.user_id)
        return WearerData.objects.create(**validated_data)


class WearerEventSerializer(serializers.Serializer):
    nowDate = serializers.DateField(read_only=True)
    nowTime = serializers.TimeField(read_only=True)
    fallEvent = serializers.CharField(max_length=1)
    heartEvent = serializers.CharField(max_length=1)

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

    def create(self, validated_data):
        return WearerEvent.objects.create(**validated_data)
