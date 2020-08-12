from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import ugettext_lazy as _

from .managers import CustomUserManager
from random import randint
# User model customize
# 이름, 타입, 전화번호 추가해야 함.
# username, name, user_type, phone_number


class CustomUser(AbstractUser):
    # username을 초기화
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_(
            'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
        null='user'+str(randint(1, 99999)),
        # primary_key=True
    )
    name = models.CharField(_('name'), max_length=128, default='user')

    # username field를 제외한 나머지 항목 중 빈칸으로 남기면 안되는 걸 required fields에서 명시해줄 수 있음
    # confirmpw 왜 있어야 superuser 생성 되는 지 모르겠음.: 이건 나중에 정리하기
    confirmpw = models.CharField(
        _('confirmpw'), max_length=128, default='0000')
    user_type = models.CharField(_('user type'), max_length=1, default='W')
    phone_number = models.CharField(
        _('phone number'), max_length=11, default='01000000000')
    # phone_num = models
    REQUIRED_FIELDS = ['name', 'confirmpw', 'phone_number', 'user_type', ]

    # objects: `objects = UserManager()` 재정의한 것
    objects = CustomUserManager()

    def __str__(self):
        if not self.username or type(self.username) != str:
            return self.email
        return self.username


class WPCouple(models.Model):
    # db 양상 지켜보기!!!
    wearer = models.ForeignKey(
        to=CustomUser, related_name='wearee', on_delete=models.CASCADE)
    protector = models.ForeignKey(
        to=CustomUser, related_name='protectee', on_delete=models.CASCADE)
