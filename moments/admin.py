from django.contrib import admin
from .models import Moment, Leap

@admin.register(Moment)
class MomentAdmin(admin.ModelAdmin):
    list_display = ("publisher", "timestamp", "archive")

@admin.register(Leap)
class LeapAdmin(admin.ModelAdmin):
    list_display = ("id", "moment", "user", "timespan")
