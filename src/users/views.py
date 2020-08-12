from django.shortcuts import render

# Create your views here.
from rest_auth.views import LoginView
from .models import CustomUser

# username, name, user_type, phone_number


class CustomLoginView(LoginView):
    # LoginView의 자식 클래스
    def get_response(self):
        # get_response override
        orginal_response = super().get_response()
        # print(self.user.username, self.user.name,
        #   self.user.user_type, self.user.phone_number)
        # print(type(self.user.username))
        mydata = {"userdata":
                  {"username": self.user.username,
                   "name": self.user.name,
                   "user_type": self.user.user_type,
                   "phone_number": self.user.phone_number},
                  "status": "success"}
        # print(type(orginal_response.data))
        # **아래가 중요한 코드**
        orginal_response.data.update(mydata)
        return orginal_response
