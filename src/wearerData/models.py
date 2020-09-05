from django.db import models
from users.models import CustomUser
# Create your models here.
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone


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


class WearerEvent(models.Model):
    # 착용자 이벤트 관련 모델, 푸시알림 관련
    user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE)
    nowDate = models.DateField(
        _('nowTime'), default=timezone.now().date(), null=True)
    nowTime = models.TimeField(
        _('nowTime'), default=timezone.now().time(), null=True)
    # 낙상이벤트
    fallEvent = models.BooleanField(default=False, null=True)
    # 부정맥이벤트
    heartEvent = models.BooleanField(default=False, null=True)


class WearerStats(models.Model):
    # 착용자 데이터 중 당일로부터 7일 전까지의 데이터는 wearerData에서 삭제, 당일 제외한 모든 데이터는 wearerStats에 통계값과 날짜만 저장.
    user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE)
    nowDate = models.DateField(
        _('now date'), default=timezone.now().date(), null=True)

    heartRate_max = models.IntegerField(_('day heart rate max'))
    heartRate_min = models.IntegerField(_('day heart rate min'))
    heartRate_avg = models.IntegerField(_('day heart rate avg'))

    sound_max = models.IntegerField(_('day sound max'))
    sound_avg = models.IntegerField(_('day sound avg'))
    sound_min = models.IntegerField(_('day sound min'))

    temp_max = models.IntegerField(_('temp rate max'))
    temp_avg = models.IntegerField(_('temp rate avg'))
    temp_min = models.IntegerField(_('temp rate min'))

    humid_max = models.IntegerField(_('humid rate max'))
    humid_avg = models.IntegerField(_('humid rate avg'))
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
