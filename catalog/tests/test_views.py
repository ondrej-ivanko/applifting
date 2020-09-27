import pytest
from builtins import breakpoint
from faker import Faker
from django.urls import reverse
from rest_framework.serializers import ValidationError
from catalog.models import Product, PriceStamp
from catalog.exceptions import CustomValidationError
from catalog.tests.factories import ProductFactory, OfferFactory, PriceStampFactory


faker = Faker(locale="en-US")


class MockResponse:
    def __init__(self, status_code):
        self.status_code = status_code

    def raise_for_status(self):
        pass


@pytest.mark.django_db
class TestProduct:
    @pytest.fixture(autouse=True)
    def get_item_guid(self):
        products = ProductFactory.create_batch(
            name="example_name", description="description", size=20
        )
        self.product_guid = products[0].guid
        yield self.product_guid

    @pytest.fixture(autouse=True)
    def setup_client(self, client):
        self.client = client
        yield self.client

    def test_create_new_product(self, mocker):
        m = mocker.MagicMock()
        m(
            "catalog.serializers.requests.post",
            return_value=MockResponse(200),
            autospec=True,
        )
        response = self.client.post(
            "/products",
            data={"name": "some name", "description": "fsdfafdfsf"},
            format="json",
        )
        assert response.status_code == 201
        assert isinstance(Product.objects.get(name="some name"), Product)
        m.assert_called_once()

    def test_list_products(self):
        count = Product.objects.all().count()
        response = self.client.get("/products")
        assert response.status_code == 200
        assert len(response.json()["results"]) == count
        for item in response.json()["results"]:
            for k, v in item.items():
                if k == "name":
                    assert v == "example_name"
                if k == "description":
                    assert v == "description"

    def test_get_product(self):
        response = self.client.get(
            reverse("products-detail", args=(self.product_guid,))
        )
        assert response.status_code == 200
        assert response.json()["guid"] == str(self.product_guid,)

    def test_delete_product(self):
        response = self.client.delete(
            reverse("products-detail", args=(self.product_guid,))
        )
        count = Product.objects.all().count()
        assert response.status_code == 204
        assert count == 19
        assert pytest.raises(
            Product.DoesNotExist, Product.objects.get, guid=self.product_guid
        )
        assert Product.objects.filter(guid=self.product_guid).exists() == False

    def test_patch_product(self):
        url = reverse("products-detail", args=(self.product_guid,))
        response = self.client.patch(
            url,
            data={"name": "AVIA", "description": "another_description"},
            content_type="application/json",
        )
        assert response.status_code == 200
        assert Product.objects.get(guid=self.product_guid).name == "AVIA"


@pytest.mark.django_db
class TestPriceHistory:
    @pytest.fixture(autouse=True)
    def inject_offers_pricestamps(self):
        o = OfferFactory()
        pricestamps = PriceStampFactory.create_batch(offer=o, size=20)
        # rewritting timestamp attr, because pricestamp is created with unchangeable default value
        # of current date time.
        for stamp in pricestamps:
            stamp.timestamp = faker.date_time_between(start_date="-60y")
            stamp.save(update_fields=["timestamp"])
        self.offers_guid, self.offers_id = o.guid, o.offers_id
        yield self.offers_guid, self.offers_id

    @pytest.fixture(autouse=True)
    def setup_client(self, client):
        self.client = client
        yield self.client

    @pytest.mark.parametrize(
        "start_date,end_date,expected",
        [
            ("1950-01-05T15:44:22", "2002-12-15T10:00:00", 200),
            ("1952-01-05T15:44:22", "2025-12-15T10:00:00", 400,),
            ("2000-01-05T15:44:22", "1980-12-15T10:00:00", 400,),
            ("", "", 400,),
        ],
    )
    def test_date_passes_priceviewset(self, start_date, end_date, expected):
        url = reverse("price_history-detail", args=(self.offers_guid,))
        response = self.client.get(
            url, {"price_initial_date": start_date, "price_final_date": end_date}
        )
        assert PriceStamp.objects.all().count() == 20

        if start_date == "1950-01-05T15:44:22":
            expected_pricestamps = PriceStamp.objects.filter(
                timestamp__range=[start_date, end_date]
            )
            assert response.status_code == expected
            # have to remove one result, because it contains 'price_differential' and 'offer_guid'
            assert len(response.json()) - 1 == expected_pricestamps.count()
            # expected price_differential, rounder down to 3 decimal places
            differential = 100 * (
                expected_pricestamps.last().price / expected_pricestamps.first().price
                - 1
            )
            differential = round(differential, 3)
            differential = (
                f"+{differential} %" if differential > 0 else f"{differential} %"
            )
            assert differential == response.json()[-1]["price_differential"]
            assert self.offers_id == response.json()[-1]["offers_id"]
        elif end_date == "2025-12-15T10:00:00":
            assert response.status_code == expected
            assert pytest.raises(CustomValidationError)
            assert response.json()[0]["code"] == "DATES_SET_IN_FUTURE"
        elif end_date == "1980-12-15T10:00:00":
            assert response.status_code == expected
            assert pytest.raises(CustomValidationError)
            assert response.json()[0]["code"] == "DATES_CONFLICT"
        else:
            assert response.status_code == expected
            assert pytest.raises(ValidationError)
            assert (
                "Datetime has wrong format"
                in response.json()["price_initial_date"][0]["message"]
                and "Datetime has wrong format"
                in response.json()["price_final_date"][0]["message"]
            )
