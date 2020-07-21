from users.models import CustomUser
from django.conf import settings
from rest_framework import serializers, exceptions
from rest_framework.serializers import raise_errors_on_nested_writes, model_meta
import traceback

from django.utils.translation import ugettext_lazy as _
from allauth.account.adapter import get_adapter
from allauth.utils import get_username_max_length
from allauth.account import app_settings as allauth_settings

from rest_auth.serializers import LoginSerializer


class UserRegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=get_username_max_length(),
        min_length=allauth_settings.USERNAME_MIN_LENGTH,
        required=allauth_settings.USERNAME_REQUIRED
    )
    password = serializers.CharField(write_only=True)
    # confirmpw = serializers.CharField(write_only=True)
    user_type = serializers.CharField(write_only=True)
    name = serializers.CharField(write_only=True)
    phone_number = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'password',
                  'user_type', 'name', 'phone_number']

    def create(self, validated_data):

        raise_errors_on_nested_writes('create', self, validated_data)

        ModelClass = self.Meta.model

        # Remove many-to-many relationships from validated_data.
        # They are not valid arguments to the default `.create()` method,
        # as they require that the instance has already been saved.
        info = model_meta.get_field_info(ModelClass)
        many_to_many = {}
        for field_name, relation_info in info.relations.items():
            if relation_info.to_many and (field_name in validated_data):
                many_to_many[field_name] = validated_data.pop(field_name)

        try:
            instance = ModelClass._default_manager.create_user(
                **validated_data)
        except TypeError:
            tb = traceback.format_exc()
            msg = (

                (
                    ModelClass.__name__,
                    ModelClass._default_manager.name,
                    ModelClass.__name__,
                    ModelClass._default_manager.name,
                    self.__class__.__name__,
                    tb
                )
            )
            raise TypeError(msg)

        # Save many-to-many relationships after the instance is created.
        if many_to_many:
            for field_name, value in many_to_many.items():
                field = getattr(instance, field_name)
                field.set(value)

        return instance

    def validate_username(self, username):
        username = get_adapter().clean_username(username)
        return username
    # valitdate_password1, validate, get_cleaned_data는 rest-auth의 RegisterSerializer에서 가져온 코드

    def validate_password1(self, password):
        return get_adapter().clean_password(password)

    def validate(self, data):
        # if data['password'] != data['confirmpw']:
        #     raise serializers.ValidationError(
        #         _("The two password fields didn't match."))
        # 아래 코드는 user_type이 a,b,A,B 중 하나가 아닐 경우 error raise하도록 하는 것
        # customized code
        if data['user_type'] not in ['A', 'B', 'a', 'b']:
            raise serializers.ValidationError(
                _('user_type should be A or B')
            )
        return data

    def get_cleaned_data(self):
        # customized code: email, password, user_type만 사용하도록.
        return {
            # 'username': self.validated_data.get('username', ''),
            'username': self.validated_data.get('username', ''),
            'name': self.validated_data.get('name', ''),
            'password': self.validated_data.get('password', ''),
            'user_type': self.validated_data.get('user_type', ''),
            'phone_number': self.validated_data.get('phone_number', '')
        }

    def save(self, request):
        # rest-auth tutorial에 따라 The custom REGISTER_SERIALIZER must define a def save(self, request) method that returns a user model instance를 구현
        # 모든 코드는 rest-auth의 registerSerializer에서 긁어와 에러 나는 부분들만 주석처리한 것이다.
        assert hasattr(self, '_errors'), (
            'You must call `.is_valid()` before calling `.save()`.'
        )

        assert not self.errors, (
            'You cannot call `.save()` on a serializer with invalid data.'
        )

        # Guard against incorrect use of `serializer.save(commit=False)`
        # assert 'commit' not in request, (
        # "'commit' is not a valid keyword argument to the 'save()' method. "
        # "If you need to access data before committing to the database then "
        # "inspect 'serializer.validated_data' instead. "
        # "You can also pass additional keyword arguments to 'save()' if you "
        # "need to set extra attributes on the saved model instance. "
        # "For example: 'serializer.save(owner=request.user)'.'"
        # )

        assert not hasattr(self, '_data'), (
            "You cannot call `.save()` after accessing `serializer.data`."
            "If you need to access data before committing to the database then "
            "inspect 'serializer.validated_data' instead. "
        )

        validated_data = dict(
            list(self.validated_data.items())
            # list(request.items())
        )

        if self.instance is not None:
            self.instance = self.update(self.instance, validated_data)
            assert self.instance is not None, (
                '`update()` did not return an object instance.'
            )
        else:
            self.instance = self.create(validated_data)
            assert self.instance is not None, (
                '`create()` did not return an object instance.'
            )

        return self.instance
