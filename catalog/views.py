from catalog.models import Product, Offer
from catalog import serializers
from rest_framework import viewsets, generics


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer
    lookup_field = "guid"


class PriceHistoryVisualizationViewSet(generics.GenericAPIView):
    queryset = Offer.objects.all()
    serializer_class = serializers.OfferSerializer
    lookup_field = "guid"

