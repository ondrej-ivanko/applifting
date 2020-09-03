import os
from django.test import TestCase
from django.urls import reverse
from catalog.models import Product
from .factories import ProductFactory, OfferFactory
from applifting.tasks import update_product_with_offers


class ProductTest(TestCase):
    def setUp(self):
        for _ in range(20):
            Product.objects.create(name="example_name", description="description")
        self.item_guid = Product.objects.first().id

    def test_list_products(self):
        count = Product.objects.all().count()
        response = self.client.get("/products")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), count)
        for k, v in response.json()[0].items():
            if k == "name":
                self.assertEqual(v, "example_name")
            if k == "description":
                self.assertEqual(v, "description")

    def test_get_product(self):
        response = self.client.get(
            reverse("products-detail", args=(str(self.item_guid),))
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["id"], str(self.item_guid))

    def test_delete_product(self):
        response = self.client.delete(
            reverse("products-detail", args=(str(self.item_guid),))
        )
        count = Product.objects.all().count()
        self.assertEqual(response.status_code, 204)
        self.assertEqual(count, 19)
        self.assertTrue(Product.DoesNotExist, Product.objects.filter(id=self.item_guid))

    def test_patch_product(self):
        url = reverse("products-detail", args=(str(self.item_guid),))
        response = self.client.patch(
            url,
            data={"name": "AVIA", "description": "another_description"},
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Product.objects.get(id=self.item_guid).name, "AVIA")

    def test_post_new_product(self):
        response = self.client.post(
            "/products",
            data={"name": "some name", "description": "fsdfafdfsf"},
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Product.objects.filter(name="some name").exists())

    def test_loop_function(self):
        pass

    def test_update_product_with_offers(self):
        OfferFactory.create_batch(20)
        update_product_with_offers()
