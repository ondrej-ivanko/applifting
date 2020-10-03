import pytest
import random
from copy import deepcopy
from catalog.models import PriceStamp, Product
from catalog.tests.factories import ProductFactory
from catalog.tasks import get_offer_pricestamps_for_all_products


offers = [{"id": random.randint(1, 100000), "price": 1500, "items_in_stock": 10} for i in range(5)]


class MockResponse:
    def __init__(self, status_code, no_offers=False):
        self.status_code = status_code
        self.no_offers = no_offers
        self.reason = b'Not Found' if 400 <= status_code <= 500 else None

    def json(self):
        if self.no_offers:
            return []
        return deepcopy(offers)


@pytest.mark.django_db
class TestCeleryTasks:

    def test_get_offer_pricestamps_for_all_products_no_product(self):
        result = get_offer_pricestamps_for_all_products()
        assert result == None

    
    def test_get_offer_pricestamps_for_all_products_exception(self, mocker):
        m = mocker.patch("requests.get",
            side_effect=Exception,
            autospec=True,
        )
        product = ProductFactory()
        get_offer_pricestamps_for_all_products()
        assert pytest.raises(Exception)
        assert product.offers.all().count() == 0


    def test_get_offer_pricestamps_for_all_products_bad_response(self, mocker):
        m = mocker.patch("requests.get",
            return_value=MockResponse(404),
            autospec=True,
        )
        product = ProductFactory()
        get_offer_pricestamps_for_all_products()
        assert product.offers.all().count() == 0


    def test_get_offer_pricestamps_for_all_products_no_offers(self, mocker):
        m = mocker.patch("requests.get",
            return_value=MockResponse(200, no_offers=True),
            autospec=True,
        )
        product = ProductFactory()
        result = get_offer_pricestamps_for_all_products()
        assert result == None
        assert product.offers.all().count() == 0
        

    def test_get_offer_pricestamps_for_all_products_offer_created(self, mocker):
        m = mocker.patch("requests.get",
            return_value=MockResponse(200),
            autospec=True,
        )
        product = ProductFactory()
        get_offer_pricestamps_for_all_products()
        assert product.offers.all().count() == 5
        assert PriceStamp.objects.all().count() == 5
