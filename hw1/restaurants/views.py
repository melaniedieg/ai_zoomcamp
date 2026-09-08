from django.shortcuts import render

from .models import Restaurant


def restaurant_list(request):
    restaurants = Restaurant.objects.all()
    return render(request, "restaurants/restaurant_list.html", {"restaurants": restaurants})
