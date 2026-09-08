from django.test import TestCase
from django.urls import reverse

from .models import Restaurant


class SanityTests(TestCase):
    def test_true_is_true(self):
        self.assertTrue(True)


class RestaurantListViewTests(TestCase):
    def setUp(self):
        self.restaurant = Restaurant.objects.create(
            name="Joe's Pizza",
            borough="Manhattan",
            cuisine="Pizza",
            address="7 Carmine St, 10014",
            external_id="12345",
        )

    def test_list_page_returns_200(self):
        response = self.client.get(reverse("restaurants:restaurant_list"))
        self.assertEqual(response.status_code, 200)

    def test_list_page_uses_expected_template(self):
        response = self.client.get(reverse("restaurants:restaurant_list"))
        self.assertTemplateUsed(response, "restaurants/restaurant_list.html")

    def test_list_page_displays_restaurant_details(self):
        response = self.client.get(reverse("restaurants:restaurant_list"))
        self.assertContains(response, "Joe&#x27;s Pizza")
        self.assertContains(response, "Manhattan")
        self.assertContains(response, "Pizza")
        self.assertContains(response, "7 Carmine St, 10014")

    def test_list_page_shows_empty_state_with_no_restaurants(self):
        Restaurant.objects.all().delete()
        response = self.client.get(reverse("restaurants:restaurant_list"))
        self.assertContains(response, "No restaurants found.")
