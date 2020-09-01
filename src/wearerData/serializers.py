
from rest_framework import serializers, exceptions
from .models import WearerData


# TODO serializers 채우기
# TODO login한 상태에서 self.user로 굳이 serializer에서 명시하지 않아도 되는 지.(이 경우 view에서 그냥 추가해 주면 되는 건 지)

class WearerDataSerializer(serializers.Serializer):
    nowTime = serializers.DateTimeField(read_only=True)
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

    # override
    # def update(self, instance, validated_data):
    #     """
    #     Update and return an existing instance, given the validated data.
    #     """
    #     instance.wearer = validated_data.get('wearer', instance.wearer)
    #     instance.protector = validated_data.get(
    #         'protector', instance.protector)
    #     instance.save()
    #     return instance
