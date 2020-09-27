from pytest_factoryboy import register
from .factories import ProductFactory, OfferFactory, PriceStampFactory

register(ProductFactory)
register(OfferFactory)
register(PriceStampFactory)
