import os
import requests
import logging
from django.conf import settings

from catalog.models import Product, Offer, PriceStamp
from catalog.exceptions import CustomValidationError
from rest_framework import serializers

logger = logging.getLogger(__name__)

BASE_URL = settings.BASE_URL


class PriceStampSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceStamp
        fields = ("timestamp", "price")


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("guid", "name", "description")

    @staticmethod
    def register_new_product(new_product_data):
        offers_access_token = os.getenv("access_token")
        response = requests.post(
            f"{BASE_URL}/products/register",
            json=new_product_data,
            headers={"Bearer": offers_access_token},
        )
        response.raise_for_status()

    def create(self, validated_data):
        instance = super().create(validated_data)
        validated_data["id"] = str(instance.guid)
        self.register_new_product(validated_data)
        return instance


class OfferSerializer(serializers.ModelSerializer):
    price_history = PriceStampSerializer(many=True)

    class Meta:
        model = Offer
        fields = ("price", "items_in_stock", "price_history")
