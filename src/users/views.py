from django.shortcuts import render

# Create your views here.
from rest_auth.views import LoginView
from .models import CustomUser, LinkedUser
from rest_framework.viewsets import ModelViewSet

from .serializers import LinkedUserSerializer


class CustomLoginView(LoginView):
    # url: /custom/login
    # LoginView의 자식 클래스
    def get_response(self):
        '''
        return updated data, which includes 
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
                    "phone_number": u.protector.phone_number
                }
            else:
                linked_users_dict[str(i)] = {
                    "username": u.wearer.username,
                    "phone_number": u.wearer.phone_number
                }

        return linked_users_dict


class LinkedUserViewSet(ModelViewSet):
    # url: /linkedUser/
    # TODO post 직후 get response에서 추가한 LinkedUser.objects.all()의 모든 내용(username, phone_number)을 get할 수 있게 한다: viewset, apiview 등 중에서 뭘 써야 할 지 더 고민하기
    # TODO /linkedUser/publicPost/ 같이 등록되어있는 linkedUser 인스턴스들을 다 알려주지 않는 방향으로 하기.
    queryset = LinkedUser.objects.all()
    serializer_class = LinkedUserSerializer
