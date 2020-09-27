import factory
import string
import uuid
from catalog.models import Offer, Product, PriceStamp


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    guid = factory.LazyFunction(lambda: uuid.uuid4())
    name = factory.Faker("name")
    description = factory.Faker(
        "lexify", text="????????????????????????????", letters=string.ascii_letters
    )

    @classmethod
    def create(cls, **kwargs):
        """
        By default, creates a Product with no Offers. To create a non-empty Product pass `num_items`
        which defines how many Offer items a Product will have.
        """
        num_items = int(kwargs.pop("num_items", 0))
        obj = super().create(**kwargs)
        # create_batch method performs INSERT query for every created object, so creating product with
        # big amount of offers may take some time.
        OfferFactory.create_batch(size=num_items, product=obj)
        return obj


class PriceStampFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PriceStamp

    price = factory.Faker(
        "pydecimal",
        right_digits=2,
        left_digits=6,
        positive=True,
        min_value=1,
        max_value=999999,
    )


class OfferFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Offer

    guid = factory.LazyFunction(lambda: uuid.uuid4())
    offers_id = factory.Faker("pyint", min_value=1, max_value=99999999)
    price = factory.Faker(
        "pydecimal",
        right_digits=2,
        left_digits=6,
        positive=True,
        min_value=1,
        max_value=999999,
    )
    items_in_stock = factory.Faker("pyint", min_value=1, max_value=20)
    product = factory.SubFactory(ProductFactory)
