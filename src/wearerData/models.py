from django.db import models
from users.models import CustomUser
# Create your models here.
from django.utils.translation import ugettext_lazy as _


class WearerData(models.Model):
    user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE)
    time = models.TimeField(_('nowTime'), auto_now=True)
    tempHumid = models.CharField(_('temp&humid_sensor'), max_length=150)
    earthMag = models.CharField(_('earthMag_sensor'), max_length=150)
    atmosPress = models.CharField(
        _('atmospherePressure_sensor'), max_length=150)
    gyro = models.CharField(_('gyro_sensor'), max_length=150)
    accel = models.CharField(_('accelerate_sensor'), max_length=150)
    heartRate = models.CharField(_('heartRate_sensor'), max_length=150)
    sound = models.CharField(_('sound_sensor'), max_length=150)
    vibrate = models.CharField(_('vibrate_sensor'), max_length=150)


'''
온습도센서: tempHumid
지자계센서: earthMag
기압 센서: atmosPress
자이로센서: gyro
가속도샌서: accel
심박: heartRate
사운드센서: sound
진동: vibrate
'''
