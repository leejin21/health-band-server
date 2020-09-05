from django.shortcuts import render
from django.core.exceptions import ValidationError
from django.http import Http404

# Create your views here.
from rest_auth.views import LoginView
from .models import CustomUser, LinkedUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView, UpdateAPIView

from rest_auth.models import TokenModel

from .serializers import LinkedUserSerializer, UserEditFcmTokenSerializer
from datetime import datetime, timedelta


class CustomLoginView(LoginView):
    # url: /custom/login
    # LoginView의 자식 클래스
    def get_response(self):
        '''
        overrided method, customized by
        returning updated data, which includes
        userdata(username, name, user_type, phone_number),
        linked_users(i: username, phone_number),
        status
        '''

        # 회원가입 이후 session 부여: stats로 데이터 옮겼는 지
        self.request.session['removedDay'] = datetime.now().date()

        orginal_response = super().get_response()

        mydata = {"userdata":
                  {"username": self.user.username,
                   "name": self.user.name,
                   "user_type": self.user.user_type,
                   "phone_number": self.user.phone_number,
                   "fcm_token": self.user.fcm_token},
                  "linked_users": self.find_linked_users(self.user),
                  "status": "success"}
        # print(type(orginal_response.data))
        # **아래가 중요한 코드**
        orginal_response.data.update(mydata)
        return orginal_response

    def find_linked_users(self, User):
        '''
        return dict of
        {"i":
            {
            "username": user.self.all()[i].other.username,
            "name": user.self.all()[i].other.name,
            "phone_number": user.self.all()[i].other.phone_number
            }
        }
        '''
        linked_users_list = User.wearee.all(
        ) if User.user_type == "W" else User.protectee.all()

        linked_users_dict = dict()

        # User.protectee.all()

        for i, u in enumerate(linked_users_list):
            if User.user_type == "W":
                linked_users_dict[str(i)] = {
                    "username": u.protector.username,
                    "name": u.protector.name,
                    "phone_number": u.protector.phone_number
                }
            else:
                linked_users_dict[str(i)] = {
                    "username": u.wearer.username,
                    "name": u.wearer.name,
                    "phone_number": u.wearer.phone_number
                }

        return linked_users_dict


class LinkedUserPostView(CreateAPIView):
    # url: /linkedUser/post/
    # TODO 로그인한 유저가 스스로와 연관된 유저만 추가할 수 있다는 security error 설정 넣기
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    # FIXED: 위 코드 떄문에 계속 Anonymous User 관련 오류 떴었는데, 이는 self.request.user을 쓰기 위해서는 `authentication_classes = [어쩌고]`로 header에 숨겨져 있는 token을 찾아내는 코드(재료)가 필요하기 때문인 것으로 추정된다.

    queryset = LinkedUser.objects.all()
    serializer_class = LinkedUserSerializer
    # overrided method

    def create(self, request, *args, **kwargs):
        '''
        Overrided method.
        Instead of returning wearer and protector usernames, this returns newLinkedUser(loginned user's newly linked user)'s information(username, name, phone_number) and status.
        For the overriding, I copied all of the original create() method's code and instead of returning the Response itself, I customized the Response.data which type is in dict form.

        The reason I copied all of the original create() method is that I could not use serializer itself if I simply called super().create(). However, I have no aware of security issues, so using super() could be right.
        '''

        # create() method로 return하는 Response에는 data가 initial data와 동일, 변형하고 저장한 validated_data와 다르기 때문에 override해 줘야 함.

        # SECTION original method
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        original_response = Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        # SECTION overriding code

        if self.request.user.user_type == "W":
            # loginned user type == wearer
            linkedUser = serializer.validated_data['protector']
        else:
            # loginned user type == protector
            linkedUser = serializer.validated_data['wearer']

        # customizing the original_response.data
        update_data = {
            "newlinkedUser": {
                "username": linkedUser.username,
                "name": linkedUser.name,
                "user_type": linkedUser.user_type,
                "phone_number": linkedUser.phone_number
            },
            "status": "success"
        }
        # original_response.data.clear()
        original_response.data.update(update_data)

        return original_response


class UserFcmTokenPostView(UpdateAPIView):
    # UserDetailsView 대신 그냥 PutRetrieve? 관련 뷰 오버라이딩하기
    serializer_class = UserEditFcmTokenSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = CustomUser.objects.all()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.fcm_token = self.request.data.get('fcm_token')
        instance.save()

        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_update(serializer)

        return Response(serializer.data)

    def get_object(self):
        """
        Returns the object the view is displaying.
        Overrided the code by not using lookup_url_kwarg, and gets the object by self username(using the token)
        """
        queryset = self.filter_queryset(self.get_queryset())

        # May raise a http404 error if obj not exists or its number is >= 2.
        obj = get_object_or_404(queryset, username=self.request.user.username)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj


def get_object_or_404(queryset, **filter_kwargs):
    """
    Overrided Code: from django.shortcuts, get_object_or_404
    gets queryset by filter_kwargs.
    """
    try:
        return queryset.get(**filter_kwargs)
    except queryset.model.DoesNotExist:
        raise Http404('No %s matches the given query or it has too much querys.' %
                      queryset.model._meta.object_name)
