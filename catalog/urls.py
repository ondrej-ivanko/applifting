from django.urls import path
from rest_framework.routers import DefaultRouter
from catalog.views import ProductViewSet, PriceHistoryVisualizationViewSet


router = DefaultRouter(trailing_slash=False)

router.register("products", ProductViewSet, basename="products"),
router.register(
    "price-history", PriceHistoryVisualizationViewSet, basename="price_history"
)

urlpatterns = [] + router.urls
