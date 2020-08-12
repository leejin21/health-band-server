from django.contrib import admin
from .models import CustomUser, WPCouple
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(WPCouple)
