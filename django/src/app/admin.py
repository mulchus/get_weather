from django.contrib import admin

from app.models import City


@admin.register(City)
class Citydmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
