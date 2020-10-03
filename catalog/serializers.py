import os
import requests
import logging
from django.utils import timezone
from django.conf import settings
from rest_framework import serializers

from catalog.models import Product, PriceStamp
from catalog.exceptions import CustomValidationError
from applifting.utils import check_and_get_offers_token

logger = logging.getLogger(__name__)

BASE_URL = settings.BASE_URL


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("guid", "name", "description")
        read_only_fields = ("guid",)

    @staticmethod
    def register_new_product(new_product_data):
        offers_access_token = check_and_get_offers_token()
        response = requests.post(
            f"{BASE_URL}/products/register",
            json=new_product_data,
            headers={"Bearer": offers_access_token},
        )
        response.raise_for_status()
        if not response.json().get("id"):
            raise CustomValidationError(
                "We have received unexpected response form Offers service", "UNEXPECTED_RESPONSE"
            )

    def create(self, validated_data):
        instance = super().create(validated_data)
        validated_data["id"] = str(instance.guid)
        self.register_new_product(validated_data)
        return instance


class DateTimeStampSerializer(serializers.Serializer):
    price_initial_date = serializers.DateTimeField(write_only=True)
    price_final_date = serializers.DateTimeField(write_only=True)

    class Meta:
        fields = ("price_initial_date", "price_final_date")

    def validate(self, attrs):
        init = attrs.get("price_initial_date")
        final = attrs.get("price_final_date")
        if final < init:
            raise CustomValidationError(
                "price_initial_date must be older than price_final_date",
                "DATES_CONFLICT",
            )
        elif final > timezone.now():
            raise CustomValidationError(
                "Dates must be less than curren date and time", "DATES_SET_IN_FUTURE"
            )
        return attrs


class PriceStampSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceStamp
        fields = ("timestamp", "price")
        read_only_fields = ("__all__",)
