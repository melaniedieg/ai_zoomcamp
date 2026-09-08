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
