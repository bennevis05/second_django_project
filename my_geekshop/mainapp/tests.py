from django.core.management import call_command
from django.test import TestCase
from django.test.client import Client

from authnapp.models import ShopUser
from mainapp.models import Product, ProductCategory


class TestMainappSmoke(TestCase):
    fixtures = [
        "categories",
        "products",
        "admin",
    ]

    def setUp(self):
        self.client = Client()

    def test_fixtures_load(self):
        # Check fixtures loading
        self.assertGreater(ProductCategory.objects.count(), 0)
        self.assertGreater(Product.objects.count(), 0)

    def test_mainapp_urls(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

        response = self.client.get("/contact/")
        self.assertEqual(response.status_code, 200)

        response = self.client.get("/catalog/")
        self.assertEqual(response.status_code, 200)

        response = self.client.get("/catalog/1/")
        self.assertEqual(response.status_code, 200)

        # for category in ProductCategory.objects.all():
        #     response = self.client.get(f"/products/category/{category.pk}/")
        #     self.assertEqual(response.status_code, 200)

        # for product in Product.objects.all():
        #     response = self.client.get(f"/products/product/{product.pk}/")
        #     self.assertEqual(response.status_code, 200)

class ProductsTestCase(TestCase):
    def test_product_print(self):
        product_1 = Product.objects.get(name="Longines HydroConquest L3.740.4.96.6")
        product_2 = Product.objects.get(name="Longines La Grande Classique L4.209.4.58.6")
        self.assertEqual(str(product_1), "Longines HydroConquest L3.740.4.96.6 (Мужские часы)")
        self.assertEqual(str(product_2), "Longines La Grande Classique L4.209.4.58.6 (Женские часы)")

    def test_product_get_items(self):
        product_1 = Product.objects.get(name="Longines HydroConquest L3.740.4.96.6")
        product_2 = Product.objects.get(name="Longines La Grande Classique L4.209.4.58.6")

        products_as_class_method = set(product_1.get_items())
        products = set([product_1, product_2])

        self.assertIsNotNone(products_as_class_method.intersection(products))
