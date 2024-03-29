from django.contrib import admin
from .models import Story, StoryLodger


@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ["id", "file", "storylodger", "time"]

@admin.register(StoryLodger)
class StoryLodgerAdmin(admin.ModelAdmin):
    list_display = ["id", "user"]