from django.contrib import admin
from .models import Basket, Save


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ("id", "moment", "user")


@admin.register(Save)
class SaveAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "blog")
