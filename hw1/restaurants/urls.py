from django.urls import path

from . import views

app_name = "restaurants"

urlpatterns = [
    path("", views.restaurant_list, name="restaurant_list"),
]
