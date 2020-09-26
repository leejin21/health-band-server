from django.test import TestCase

# Create your tests here.
from users.models import CustomUser, LinkedUser

for lu in LinkedUser.objects.all():
    print(lu.wearer, lu.protector)
