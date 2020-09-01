from django.db import models
from users.models import CustomUser
# Create your models here.
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone


class WearerData(models.Model):
    user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE)
    # TODO default를 KR 시간으로 맞춰야 함
    nowTime = models.DateTimeField(
        _('nowTime'), default=timezone.now(), null=True)
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
온습도센서: tempHumid
기압 센서: atmosPress
자이로센서: gyro
가속도샌서: accel
심박: heartRate
사운드센서: sound
진동: vibrate
'''


'''
나와야 하는 값
(평균)
8/26: 20, 50, 45, 1750
8/27~31: 50, 30, 50, 2000
9/1: 20, 50, 55, 2250

(최대)
8/26: 20, 50, 50, 2000
8/27~31: 50, 30, 50, 2000
9/1: 20, 50, 55, 2250

(최소)
8/26: 20, 50, 45, 1750
8/27~31: 20, 50, 50, 2000
9/1: 20, 50, 50, 2000
'''
