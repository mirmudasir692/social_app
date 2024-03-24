from django.contrib import admin
from .models import Moment, Leaf, Fruit


@admin.register(Moment)
class MomentAdmin(admin.ModelAdmin):
    list_display = ("publisher", "timestamp", "archive")


@admin.register(Leaf)
class LeapAdmin(admin.ModelAdmin):
    list_display = ("id", "moment", "user", "timespan")


@admin.register(Fruit)
class FruitAdmin(admin.ModelAdmin):
    list_display = ["content", "user", "moment", "timespan"]
