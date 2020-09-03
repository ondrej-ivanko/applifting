"""
Runs iterative task to regularly check for new offers added to Offers Service and updates or creates
new offers to related Product accordingly if necessary.
"""
import logging
import time
import requests
from django.conf import settings
from django.db import transaction
from catalog.models import Product, Offer, PriceStamp
from applifting.utils import check_and_get_offers_token


logger = logging.getLogger(__name__)


def update_product_with_offers(product, offers):
    with transaction.atomic():
        for offer in offers:
            obj, created = Offer.objects.update_or_create(
                id=offer["id"],
                defaults={
                    "price": offer["price"],
                    "items_in_stock": offer["items_in_stock"],
                    "product": product,
                },
            )
            if created:
                logger.info("We have received a new Offer for Prodcut: %s.", product.id)
            # creating latest price snapshot
            PriceStamp.objects.create(price=offer["price"], offer=obj)


def loop():
    while True:
        products = Product.objects.all()
        offers_token = check_and_get_offers_token()
        for product in products:
            try:
                response = requests.get(
                    f"{settings.BASE_URL}/products/{product.guid}/offers",
                    data=product.guid,
                    headers=f"Bearer {offers_token}",
                )
            except Exception as exc:
                logger.error(
                    "Could not connect to Offers service because of exception: %s", exc
                )
                pass
            else:
                if response.status_code != 200:
                    logger.warning(
                        "The offers of product guid: %s cannot be updated, because of %s",
                        product.guid,
                        response.reason,
                    )
                else:
                    returned_offers = response.json()[0]
                    if returned_offers:
                        update_product_with_offers(product, returned_offers)
        time.sleep(60.0)


if __name__ == "__main__":
    loop()
