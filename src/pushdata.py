from users.models import CustomUser
from wearerData.models import WearerData, WearerMeter, WearerStats

from datetime import datetime, timedelta
from random import randint
import time

'''
HELP
* 설명
wearerdata와 wearermeter에 오늘 포함, 7일치 데이터 집어넣는 코드

* 하기 직전에 models.py에서 수정하기:

WearerData에서
nowDate = models.DateField(
        _('nowDate'), default=timezone.now().date(), null=True)
nowTime = models.TimeField(
        _('nowTime'), default=timezone.now().time(), null=True)

WearerMeter에서
nowDT = models.DateTimeField(_('now date time'), default=timezone.now)


이후 터미널에서
> python manage.py makemigrations
> python manage.py migrate

* 명령어
> python manage.py shell < pushdata.py
> cd ../clients
> python postSensor.py w3
// 실행하고 한두개 이후 바로 ctrl+C
'''

GMAIL = "@gmail.com"
w1 = "w1" + GMAIL
w2 = "w2" + GMAIL
w3 = "w3" + GMAIL

# --------------------------------------
# 변환 가능
NUM = 5
DAYS = 7
uname = w2
# --------------------------------------

today = datetime.now().date()
weekdays = [today - timedelta(days=i) for i in range(DAYS-2, -1, -1)]


user = CustomUser.objects.get(username=uname)
print("user data removed date: ", user.dataRemovedDate)
user.dataRemovedDate = datetime.now().date() - timedelta(days=2)
user.save()
print("user data removed date: ", user.dataRemovedDate)

for i in range(len(weekdays)):
    for j in range(NUM):
        TEMP = str(randint(4, 15))
        HUMID = str(randint(30, 60))
        HEARTRATE = str(randint(61, 109))
        NOW = weekdays[i]
        WearerData.objects.create(
            user=user, nowDate=NOW, temp=TEMP, humid=HUMID, heartRate=HEARTRATE)
        WearerMeter.objects.create(
            user=user, nowDT=NOW, meter=randint(100, 3000))


# 여기서 postSensor 실행 argv로 w2 삽입
print("user data removed date: ", user.dataRemovedDate)

for stats in WearerStats.objects.filter(user=user):
    print(stats.nowDate)
