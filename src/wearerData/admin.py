from django.contrib import admin
from .models import WearerData, WearerEvent, WearerStats, HeatPreEvent
# Register your models here.
admin.site.register(WearerData)
admin.site.register(WearerEvent)
admin.site.register(WearerStats)
admin.site.register(HeatPreEvent)
