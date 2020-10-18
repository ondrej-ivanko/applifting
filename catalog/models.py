import uuid
from django.db import models


class Product(models.Model):
    guid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=255)
    description = models.TextField()


class Offer(models.Model):
    guid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    offers_id = models.PositiveIntegerField(unique=True)
    price = models.DecimalField(decimal_places=2, max_digits=8)
    items_in_stock = models.PositiveIntegerField()
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="offers", to_field="guid"
    )


class PriceStamp(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(decimal_places=2, max_digits=8)
    offer = models.ForeignKey(
        Offer, on_delete=models.CASCADE, related_name="pricestamps", to_field="guid"
    )

    class Meta:
        ordering = ["timestamp"]
