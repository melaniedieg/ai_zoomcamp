from django.contrib import admin

from .models import Restaurant


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ("name", "borough", "cuisine", "address")
    search_fields = ("name", "borough", "cuisine")
