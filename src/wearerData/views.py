from django.shortcuts import render

from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.settings import api_settings

from rest_framework import status
from rest_framework.response import Response


from .models import WearerData
from .serializers import WearerDataSerializer
# Create your views here.
# TODO 여기 채우기


class WearerDataPostView(CreateAPIView):
    # url: /linkedUser/post/
    # TODO 로그인한 유저가 스스로와 연관된 유저만 추가할 수 있다는 security error 설정 넣기
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    # FIXED: 위 코드 떄문에 계속 Anonymous User 관련 오류 떴었는데, 이는 self.request.user을 쓰기 위해서는 `authentication_classes = [어쩌고]`로 header에 숨겨져 있는 token을 찾아내는 코드(재료)가 필요하기 때문인 것으로 추정된다.

    queryset = WearerData.objects.all()
    serializer_class = WearerDataSerializer
    # overrided method

    def create(self, request, *args, **kwargs):
        '''
        Overrided method. added update_data which includes status: sucess.
        '''
        # SECTION original method
        serializer = WearerDataSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        original_response = Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        # SECTION overriding code
        print(serializer.data, original_response.data)
        # customizing the original_response.data
        update_data = {
            "data": serializer.data,
            "status": "success"
        }
        original_response.data.clear()
        original_response.data.update(update_data)

        return original_response

    def perform_create(self, serializer):
        '''
        Overrided method. saves user as self.request.user to the serializer.
        '''
        serializer.save(user=self.request.user)
