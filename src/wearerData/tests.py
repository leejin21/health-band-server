from django.test import TestCase

# Create your tests here.
from users.models import CustomUser, LinkedUser
from datetime import datetime, timedelta
from wearerData.models import WearerData, WearerMeter, WearerEvent, WearerStats, HeatPreEvent, WearerLocation


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


# sensor data post

temp = '''
18, 27
18, 26
17, 24
16, 25
15, 24
17, 24
17, 24
'''

humid = '''
40, 60
42, 62
43, 58
50, 70
52, 72
47, 60
53, 69
'''

heartRate = '''
50,	90
52,	87
49,	85
55,	78
53,	92
55,	80
47,	89
'''


sound = '''
5, 100
1, 80
10, 70
20, 62
15, 68
17, 84
13, 95
'''

step = '''
1211
587
2982
2225
4521
5287
3642
'''
temp = [i.split(", ") for i in temp.split("\n")[1:-1]]
heartRate = [i.split(",\t") for i in heartRate.split("\n")[1:-1]]
humid = [i.split(", ") for i in humid.split("\n")[1:-1]]
sound = [i.split(", ") for i in sound.split("\n")[1:-1]]
step = [int(i) for i in step.split("\n")[1:-1]]

temp = [[int(i) for i in comp] for comp in temp]
heartRate = [[int(i) for i in comp] for comp in heartRate]
humid = [[int(i) for i in comp] for comp in humid]
sound = [[int(i) for i in comp] for comp in sound]

temp = [[18, 27], [18, 26], [17, 24], [16, 25], [15, 24], [17, 24], [17, 24]]
heartRate = [[50, 90], [52, 87], [49, 85],
             [55, 78], [53, 92], [55, 80], [47, 89]]
humid = [[40, 60], [42, 62], [43, 58], [50, 70], [52, 72], [47, 60], [53, 69]]
sound = [[5, 100], [1, 80], [10, 70], [20, 62], [15, 68], [17, 84], [13, 95]]
step = [1211, 587, 2982, 2225, 4521, 5287, 3642]

weekdays = [datetime.now().date() - timedelta(days=i)
            for i in range(3, -1, -1)]
w2 = CustomUser.objects.get(username="w2@gmail.com")

for i in range(len(weekdays)):
    for j in range(2):
        WearerData.objects.create(
            user=w2, nowDate=weekdays[i], temp=temp[i][j], humid=humid[i][j], heartRate=heartRate[i][j], sound=sound[i][j], stepCount=step[i])


# SECTION wearer meter add instance

w3 = CustomUser.objects.get(username="w3@gmail.com")
steps = [1000, 2000, 3000, 4000, 3000, 2000]
weekdays = [datetime.now().date() - timedelta(days=i)
            for i in range(12, 6, -1)]

for i in range(len(steps)):
    WearerMeter.objects.create(user=w3, nowDT=datetime.combine(
        weekdays[i], datetime.now().time()), meter=steps[i])
