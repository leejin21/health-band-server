from django.db import models
from users.models import CustomUser
# Create your models here.
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

import requests
import json

from .fcm_key import server_key


class WearerData(models.Model):
    user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE)
    # TODO default를 KR 시간으로 맞춰야 함
    nowDate = models.DateField(
        _('nowTime'), default=timezone.now().date(), null=True)
    nowTime = models.TimeField(
        _('nowTime'), default=timezone.now().time(), null=True)
    temp = models.CharField(_('temp_sensor'), max_length=50, default="20")
    humid = models.CharField(_('humid_sensor'), max_length=50, default='50')

    heartRate = models.CharField(_('heartRate_sensor'), max_length=50)
    sound = models.CharField(_('sound_sensor'), max_length=50)
    stepCount = models.CharField(_('stepCount'), max_length=50, default='200')


class HeatPreEvent(models.Model):
    user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE)
    nowDate = models.DateField(default=timezone.now().date(), null=True)
    a_start = models.TimeField(default=timezone.now().time(), null=True)
    b_start = models.TimeField(default=timezone.now().time(), null=True)
    c_start = models.TimeField(default=timezone.now().time(), null=True)
    eventType = models.CharField(default='N', max_length=1, null=True)


class WearerEvent(models.Model):
    # 착용자 이벤트 관련 모델, 푸시알림 관련
    user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE)
    nowDate = models.DateField(
        _('nowTime'), default=timezone.now().date(), null=True)
    nowTime = models.TimeField(
        _('nowTime'), default=timezone.now().time(), null=True)
    # 낙상이벤트
    fallEvent = models.BooleanField(default=False, null=True)
    # 부정맥이벤트: 장고로 그냥 구현해버리기.
    heartEvent = models.BooleanField(default=False, null=True)
    # 더위 먹는 이벤트 관련도 구현해 주기.
    heatIllEvent = models.CharField(default='N', max_length=1, null=True)

    def save(self, *args, **kwargs):

        if self.user.user_type == "W":
            # ids = [self.user.wearee.all()[i].protector.fcm_token for i in range(
            #     len(self.user.wearee.all()))] + [self.user.fcm_token]
            ids = [self.user.fcm_token]
            # print(ids)
            if self.fallEvent == True:
                title = "낙상 사고 발생"
                body = self.user.name + "님의 디바이스에서 낙상을 감지했습니다."
                print(ids, title, body)
                self.send_fcm_notification(ids, title, body)
            elif self.heartEvent == True:
                title = "부정맥 발생"
                body = self.user.name + "님의 디바이스에서 부정맥을 감지했습니다."
                print(ids, title, body)
                self.send_fcm_notification(ids, title, body)
            elif self.heatIllEvent != "N":
                # TODO 여기서 heatIllEvent 유형에 따라 알림 다르게 하는 코드 적어주기
                title = "일사병 위험"
                body = self.user.name + "님의 디바이스에서 일사병 위험을 감지했습니다."

        super(WearerEvent, self).save(*args, **kwargs)

    def send_fcm_notification(self, ids, title, body):
        # TODO 여기서 for문으로 여러 디바이스에 한번씩 보내거나 or python으로 여러 디바이스에게 한꺼번에 보내는 방법 찾아서 코드 짜기
        # fcm 푸시 메세지 요청 주소
        url = "https://fcm.googleapis.com/fcm/send"
        # 인증 정보(서버 키)를 헤더에 담아 전달
        headers = {
            'Authorization': 'key= ' + server_key(),
            'Content-Type': 'application/json; UTF-8',
        }

        # 보낼 내용과 대상을 지정
        # ids 존재 안하면 에러 발생하게 하기.
        for id in ids:
            content = {
                'to': id,
                'data': {
                    'title': title,
                    'message': body
                }
            }

            # json 파싱 후 requests 모듈로 FCM 서버에 요청
            response = requests.post(
                url, data=json.dumps(content), headers=headers)
            print("Status Code:", response.status_code)


class WearerStats(models.Model):
    # 착용자 데이터 중 당일로부터 7일 전까지의 데이터는 wearerData에서 삭제, 당일 제외한 모든 데이터는 wearerStats에 통계값과 날짜만 저장.
    user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE)
    nowDate = models.DateField(
        _('now date'), default=timezone.now().date(), null=True)

    heartRate_max = models.IntegerField(_('day heart rate max'))
    heartRate_min = models.IntegerField(_('day heart rate min'))
    heartRate_avg = models.FloatField(_('day heart rate avg'))

    sound_max = models.IntegerField(_('day sound max'))
    sound_avg = models.FloatField(_('day sound avg'))
    sound_min = models.IntegerField(_('day sound min'))

    temp_max = models.IntegerField(_('temp rate max'))
    temp_avg = models.FloatField(_('temp rate avg'))
    temp_min = models.IntegerField(_('temp rate min'))

    humid_max = models.IntegerField(_('humid rate max'))
    humid_avg = models.FloatField(_('humid rate avg'))
    humid_min = models.IntegerField(_('humid rate min'))

    stepCount = models.IntegerField(_('day step count'))


'''
온도: temp
습도: humid
심박: heartRate
사운드센서: sound
stepCount: vibrate
'''

'''
나와야 하는 값
(평균)
20 50 30
'''
