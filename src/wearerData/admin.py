from django.contrib import admin
from .models import WearerData, WearerEvent
# Register your models here.
admin.site.register(WearerData)
admin.site.register(WearerEvent)
