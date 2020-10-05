from collections import OrderedDict
from django.utils import timezone
from catalog.models import Product, Offer, PriceStamp
from catalog import serializers
from rest_framework import viewsets, mixins
from rest_framework.response import Response


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer
    lookup_field = "guid"


class PriceHistoryVisualizationViewSet(
    mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    queryset = Offer.objects.all()
    lookup_field = "guid"

    def _get_price_difference(self, initial_price, final_price):
        difference = round(100 * (final_price / initial_price - 1), 3)
        if initial_price < final_price:
            return f"+{difference} %"
        return f"{difference} %"

    def _get_pricestamps_and_differential(self, instance, validated_data):
        """
        Finds pricestamps between provided dates and return their rise/fall % difference.
        """
        prices_start_date, prices_end_date = (
            validated_data["price_initial_date"],
            validated_data["price_final_date"],
        )
        pricestamps_selection = instance.pricestamps.filter(
            timestamp__range=[prices_start_date, prices_end_date]
        )
        # default 0 value in case we get empty qs from pricestamps_selection
        price_differential = "0"
        if pricestamps_selection:
            price_differential = self._get_price_difference(
                pricestamps_selection.first().price, pricestamps_selection.last().price
            )
        return pricestamps_selection, price_differential

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        lookup_dates = {
            "price_initial_date": request.query_params.get("price_initial_date"),
            "price_final_date": request.query_params.get("price_final_date"),
        }
        serializer = serializers.DateTimeStampSerializer(data=lookup_dates)
        serializer.is_valid(raise_exception=True)
        (
            pricestamps_selection,
            price_differential,
        ) = self._get_pricestamps_and_differential(instance, serializer.validated_data)
        serializer = serializers.PriceStampSerializer(pricestamps_selection, many=True,)

        # adding 'price changes in given time period' and 'related offer id' as last items
        # of response, so it's not duplicated in results.
        serializer_data = serializer.data + [
            OrderedDict(
                [
                    ("price_differential", price_differential),
                    ("offers_id", instance.offers_id),
                ]
            )
        ]
        return Response(serializer_data)
