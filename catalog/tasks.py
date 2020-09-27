"""
Runs iterative task to regularly check for new offers or price updates added to 
'Offers Service' for given product. Creates new offers to related Product obj accordingly. 
Creates snapshot/pricestamp of latest price of Offer obj.
"""
import os
import logging
import requests
from builtins import breakpoint
from django.conf import settings
from django.db import transaction
from celery.schedules import crontab
from catalog.models import Product, Offer, PriceStamp
from applifting.utils import check_and_get_offers_token

logger = logging.getLogger(__name__)


def update_product_with_offers(product, offers):
    with transaction.atomic():
        for offer in offers:
            obj, created = Offer.objects.update_or_create(
                offers_id=offer["id"],
                defaults={
                    "price": offer["price"],
                    "items_in_stock": offer["items_in_stock"],
                    "product": product,
                },
            )
            if created:
                logger.info("We have received a new Offer for Product: %s.", product.id)
            # creating latest price snapshot
            PriceStamp.objects.create(price=offer["price"], offer=obj)


def get_offer_pricestamps_for_all_products():
    products = Product.objects.all()
    if not products:
        logger.info("No products to get offers for.")
        return
    offers_access_token = check_and_get_offers_token()
    for product in products:
        breakpoint()
        try:
            response = requests.get(
                f"{os.getenv('BASE_URL')}/products/{product.guid}/offers",
                headers={"Bearer": offers_access_token},
            )
        except Exception as exc:
            logger.error(
                "Could not connect to Offers service because of exception: %s", exc
            )
        else:
            if response.status_code != 200:
                logger.warning(
                    "The offers of product guid: %s cannot be retrieved, because of %s",
                    product.guid,
                    response.reason_phrase,
                )
            else:
                returned_offers = response.json()
                if not returned_offers:
                    logger.info("We do not have any offers for given product yet.")
                    return
                update_product_with_offers(product, returned_offers)
