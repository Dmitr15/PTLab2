from django.test import TestCase, Client
from shop.views import PurchaseCreate
from django.urls import reverse
from shop.models import Product, Purchase

class PurchaseCreateTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.product = Product.objects.create(name="book", price="740")
        self.url = reverse('buy', args=[self.product.id])

    def test_webpage_accessibility(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/index.html')
                
    def test_buy_page_accessibility(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/purchase_form.html')

    def test_buy_form_submission(self):
        response = self.client.post(self.url, {
            'product': self.product.id,
            'person': 'Петров',
            'address': 'Ленина 5'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Спасибо за покупку, Петров!")
        self.assertEqual(Purchase.objects.count(), 1)   