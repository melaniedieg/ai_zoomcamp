from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .models import Restaurant, WantToGo


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
    restaurants = restaurants.prefetch_related("want_to_go_flags")

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

    visitor_name = request.session.get("visitor_name", "")
    restaurants_data = []
    for restaurant in restaurants:
        flag_names = [flag.name for flag in restaurant.want_to_go_flags.all()]
        restaurants_data.append(
            {
                "restaurant": restaurant,
                "flag_names": flag_names,
                "is_flagged_by_visitor": bool(visitor_name) and visitor_name in flag_names,
            }
        )

    context = {
        "restaurants_data": restaurants_data,
        "boroughs": boroughs,
        "cuisines": cuisines,
        "query": query,
        "selected_borough": borough,
        "selected_cuisine": cuisine,
        "visitor_name": visitor_name,
    }
    return render(request, "restaurants/restaurant_list.html", context)


def set_visitor_name(request):
    next_url = request.POST.get("next") or reverse("restaurants:restaurant_list")
    if request.method == "POST":
        name = request.POST.get("visitor_name", "").strip()
        request.session["visitor_name"] = name
    return redirect(next_url)


def toggle_want_to_go(request, restaurant_id):
    next_url = request.POST.get("next") or reverse("restaurants:restaurant_list")
    if request.method != "POST":
        return redirect(next_url)

    visitor_name = request.session.get("visitor_name", "").strip()
    if not visitor_name:
        return redirect(next_url)

    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    flag, created = WantToGo.objects.get_or_create(
        restaurant=restaurant, name=visitor_name
    )
    if not created:
        flag.delete()

    return redirect(next_url)
