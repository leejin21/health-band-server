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
    # atmosPress = models.CharField(
    # _('atmospherePressure_sensor'), max_length = 150)
    # gyro = models.CharField(_('gyro_sensor'), max_length=50)
    # accel = models.CharField(_('accelerate_sensor'), max_length=50)
    heartRate = models.CharField(_('heartRate_sensor'), max_length=50)
    sound = models.CharField(_('sound_sensor'), max_length=50)
    stepCount = models.CharField(_('stepCount'), max_length=50, default='200')


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
