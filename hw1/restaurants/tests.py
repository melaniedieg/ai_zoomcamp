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


class RestaurantSearchAndFilterTests(TestCase):
    def setUp(self):
        self.pizza = Restaurant.objects.create(
            name="Joe's Pizza",
            borough="Manhattan",
            cuisine="Pizza",
            address="7 Carmine St, 10014",
            external_id="1",
        )
        self.ramen = Restaurant.objects.create(
            name="Ivan Ramen",
            borough="Manhattan",
            cuisine="Japanese",
            address="25 Clinton St, 10002",
            external_id="2",
        )
        self.diner = Restaurant.objects.create(
            name="Tom's Diner",
            borough="Brooklyn",
            cuisine="American",
            address="782 Franklin Ave, 11238",
            external_id="3",
        )

    def test_search_by_name_is_case_insensitive_and_partial(self):
        response = self.client.get(reverse("restaurants:restaurant_list"), {"q": "pizza"})
        self.assertContains(response, "Joe&#x27;s Pizza")
        self.assertNotContains(response, "Ivan Ramen")
        self.assertNotContains(response, "Tom&#x27;s Diner")

    def test_filter_by_borough(self):
        response = self.client.get(
            reverse("restaurants:restaurant_list"), {"borough": "Brooklyn"}
        )
        self.assertContains(response, "Tom&#x27;s Diner")
        self.assertNotContains(response, "Joe&#x27;s Pizza")
        self.assertNotContains(response, "Ivan Ramen")

    def test_filter_by_cuisine(self):
        response = self.client.get(
            reverse("restaurants:restaurant_list"), {"cuisine": "Japanese"}
        )
        self.assertContains(response, "Ivan Ramen")
        self.assertNotContains(response, "Joe&#x27;s Pizza")
        self.assertNotContains(response, "Tom&#x27;s Diner")

    def test_search_and_filters_combine(self):
        response = self.client.get(
            reverse("restaurants:restaurant_list"),
            {"q": "ramen", "borough": "Manhattan", "cuisine": "Japanese"},
        )
        self.assertContains(response, "Ivan Ramen")
        self.assertNotContains(response, "Joe&#x27;s Pizza")
        self.assertNotContains(response, "Tom&#x27;s Diner")

    def test_combined_filters_with_no_matches_show_empty_state(self):
        response = self.client.get(
            reverse("restaurants:restaurant_list"),
            {"borough": "Brooklyn", "cuisine": "Japanese"},
        )
        self.assertContains(response, "No restaurants found.")

    def test_selected_filter_values_are_preserved_in_the_form(self):
        response = self.client.get(
            reverse("restaurants:restaurant_list"),
            {"q": "ramen", "borough": "Manhattan", "cuisine": "Japanese"},
        )
        self.assertContains(response, 'value="ramen"')
        self.assertContains(
            response, '<option value="Manhattan" selected>Manhattan</option>'
        )
        self.assertContains(
            response, '<option value="Japanese" selected>Japanese</option>'
        )
