from django.test import TestCase

# Create your tests here.
from users.models import CustomUser
from datetime import datetime, timedelta
from wearerData.models import WearerData

u = CustomUser.objects.get(username="w3@gmail.com")
qs = WearerData.objects.order_by('nowDate').filter(
    user=u, nowDate=datetime.now().date()-timedelta(days=4))

st = []
hr = []
so = []
te = []
hu = []

for d in qs:
    print(d.nowDate)
    st.append(int(d.stepCount))
    hr.append(int(d.heartRate))
    so.append(int(d.sound))
    te.append(int(d.temp))
    hu.append(float(d.humid))

cnt = 0
for sensor in [st, hr, so, te, hu]:
    print(cnt)
    cnt += 1
    print(sum(sensor), min(sensor), max(sensor))

u.dataRemovedDate = datetime.now().date() - timedelta(days=1)
u.save()
print(u.dataRemovedDate)

'''
2020-08-27
50
40
200
20
60

2020-08-28
50
40
200
20
60

2020-08-29
50
40
200
20
60

2020-08-30
[50, 70, 90]
[30, 35, 40]
[200, 250, 300]
20
60

2020-08-31
50
40
200
20
60

2020-09-01
50
40
200
20
60

2020-09-02
0
3500
1
400 40 100
2
270 10 100
3
240 10 100
4
377.5 37.5 100.0

2020-09-03
80
40
2000
30
70


'''
