from django.test import TestCase
from django.test import Client

from shop.models import Discount


class PurchaseCreateTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_webpage_accessibility(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

class DiscountCreateTestCase(TestCase):
        def setUp(self):
            self.client = Client()

        def test_webpage_accessibility(self):
            response = self.client.get('/discount/')
            self.assertEqual(response.status_code, 200)

        def test_webpage_not_found(self):
            response = self.client.get('discount/')
            self.assertEqual(response.status_code, 404)

        def test_discount_registrate(self):
            self.client.post('/discount/',
                                        data={
                                              "total" : "0",
                                              "discount" : "0",
                                              "person" : "test1"})

            self.assertEqual("test1", Discount.objects.first().person)
            self.assertEqual(0, Discount.objects.first().discount)
            self.assertEqual(0, Discount.objects.first().total)