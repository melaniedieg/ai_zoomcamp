from django.contrib import admin

from .models import Restaurant, WantToGo


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ("name", "borough", "cuisine", "address")
    search_fields = ("name", "borough", "cuisine")


@admin.register(WantToGo)
class WantToGoAdmin(admin.ModelAdmin):
    list_display = ("name", "restaurant", "created_at")
    search_fields = ("name", "restaurant__name")
