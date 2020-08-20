from django.shortcuts import render

# Create your views here.
from rest_auth.views import LoginView
from .models import CustomUser, LinkedUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView

from rest_auth.models import TokenModel

from .serializers import LinkedUserSerializer


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
        orginal_response = super().get_response()

        mydata = {"userdata":
                  {"username": self.user.username,
                   "name": self.user.name,
                   "user_type": self.user.user_type,
                   "phone_number": self.user.phone_number},
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
            "username": user.self.all()[i].other.username
            "phone_number": user.self.all()[i].other.phone_number
            }
        }
        '''
        linked_users_list = User.wearee.all(
        ) if User.user_type == "W" else User.protectee.all()

        linked_users_dict = dict()

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


# class LinkedUserView(APIView):

    # def get(self, request, format=None):
    #     # print(self.request.user)
    #     linkedUsers = LinkedUser.objects.all()
    #     serializer = LinkedUserSerializer(linkedUsers, many=True)
    #     # print(serializer.data)
    #     return Response(serializer.data)

    # def post(self, request, format=None):
    #     serializer = LinkedUserSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
