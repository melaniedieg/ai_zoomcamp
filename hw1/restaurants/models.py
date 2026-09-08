from django.db import models


class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    borough = models.CharField(max_length=100, blank=True)
    cuisine = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=255, blank=True)
    external_id = models.CharField(max_length=50, unique=True, blank=True, null=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class WantToGo(models.Model):
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name="want_to_go_flags"
    )
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields=["restaurant", "name"], name="unique_want_to_go_per_person"
            )
        ]

    def __str__(self):
        return f"{self.name} wants to go to {self.restaurant.name}"
