"""
Runs iterative task to regularly check for new offers or price updates added to 
'Offers Service' for given product. Creates new offers to related Product obj accordingly. 
Creates snapshot/pricestamp of latest price of Offer obj.
"""
import logging
import requests
from django.conf import settings
from django.db import transaction
from django.utils import timezone
from catalog.models import Product, Offer, PriceStamp
from applifting.utils import check_and_get_offers_token

logger = logging.getLogger(__name__)


def update_product_with_offers(product, offers):
    for offer in offers:
        with transaction.atomic():
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
                PriceStamp.objects.create(price=obj.price, offer=obj)
                logger.info("Initial price stamp for new offer created.")
            else:
                latest_pricestamp = obj.pricestamps.last()
                # time_elapsed variable works like a pricestamp creation sanity check.
                # I want to limit the amount of pricestamps created, when the price effectively
                # does not change. It is unnecessary. The DB therefore does not get overwhelmed
                # with massive amount of timestamps every minute the task is run.
                time_elapsed = latest_pricestamp.timestamp - timezone.now()
                if (
                    latest_pricestamp.price != obj.price
                    or time_elapsed.seconds >= 86400
                ):
                    PriceStamp.objects.create(price=obj.price, offer=obj)
                    logger.info("Update-like price stamp created.")


def get_offer_pricestamps_for_all_products():
    products = Product.objects.all()
    if not products:
        logger.info("No products to get offers for.")
        return
    offers_access_token = check_and_get_offers_token()
    for product in products:
        try:
            response = requests.get(
                f"{settings.BASE_URL}/products/{product.guid}/offers",
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
