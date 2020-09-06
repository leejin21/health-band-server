"""health_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from allauth.account.views import confirm_email
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
# from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter

from users.views import CustomLoginView, LinkedUserPostView, UserFcmTokenPostView
from wearerData.views import WearerDataPostView, WearerEventPostView, SensorGetView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration', include('rest_auth.registration.urls')),
    url(r'^account/', include('allauth.urls')),
    url(r'custom/login/', CustomLoginView.as_view(), name='my_custom_login'),
    # path('', include(router.urls)),
    path('user/changeFcmToken/', UserFcmTokenPostView.as_view()),
    path('linkedUser/post/', LinkedUserPostView.as_view()),
    path('wearerData/post/', WearerDataPostView.as_view()),
    path('sensorData/get/', SensorGetView.as_view()),
    path('wearerEvent/post/', WearerEventPostView.as_view())
]
