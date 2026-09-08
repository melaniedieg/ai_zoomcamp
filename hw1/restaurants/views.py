from django.shortcuts import render

from .models import Restaurant


def restaurant_list(request):
    query = request.GET.get("q", "").strip()
    borough = request.GET.get("borough", "").strip()
    cuisine = request.GET.get("cuisine", "").strip()

    restaurants = Restaurant.objects.all()
    if query:
        restaurants = restaurants.filter(name__icontains=query)
    if borough:
        restaurants = restaurants.filter(borough=borough)
    if cuisine:
        restaurants = restaurants.filter(cuisine=cuisine)

    boroughs = (
        Restaurant.objects.exclude(borough="")
        .order_by("borough")
        .values_list("borough", flat=True)
        .distinct()
    )
    cuisines = (
        Restaurant.objects.exclude(cuisine="")
        .order_by("cuisine")
        .values_list("cuisine", flat=True)
        .distinct()
    )

    context = {
        "restaurants": restaurants,
        "boroughs": boroughs,
        "cuisines": cuisines,
        "query": query,
        "selected_borough": borough,
        "selected_cuisine": cuisine,
    }
    return render(request, "restaurants/restaurant_list.html", context)
