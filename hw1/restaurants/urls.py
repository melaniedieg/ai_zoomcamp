from django.urls import path

from . import views

app_name = "restaurants"

urlpatterns = [
    path("", views.restaurant_list, name="restaurant_list"),
    path("set-name/", views.set_visitor_name, name="set_visitor_name"),
    path(
        "<int:restaurant_id>/want-to-go/",
        views.toggle_want_to_go,
        name="toggle_want_to_go",
    ),
]
