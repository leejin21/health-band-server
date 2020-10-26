from users.models import CustomUser
from wearerData.models import WearerEvent

'''
HELP
'''
# ------------
# 변경 가능
# 0: 낙상, 1: 부정맥, 2: 열사병
# CASE = 0
# ------------

user = CustomUser.objects.get(username="w3@gmail.com")

we = WearerEvent.objects.create(user=user, fallEvent=True)
# we = WearerEvent(user=user, heartEvent="B")
# we = WearerEvent(user=user, heatIllEvent="B")

we.save()
