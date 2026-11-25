from django.test import TestCase
from django.urls import reverse
from shop.models import Product, Purchase

class DiscountTest(TestCase):
    def setUp(self):
        self.p1 = Product.objects.create(name="Футболка", price=1000)
        self.p2 = Product.objects.create(name="Джинсы", price=2000)
        self.url = reverse('checkout')

    def test_single_product_no_discount(self):
        response = self.client.post(self.url, {
            'person': 'Иван', 'address': 'Улица 1',
            f'product_{self.p1.id}': 1, f'product_{self.p2.id}': 0,
        })
        self.assertContains(response, "Итоговая сумма: 1000 руб.")
        self.assertNotContains(response, "скидка 10%")

    def test_same_product_multiple_times_no_discount(self):
        response = self.client.post(self.url, {
            'person': 'Иван', 'address': 'Улица 1',
            f'product_{self.p1.id}': 2, f'product_{self.p2.id}': 0,
        })
        self.assertContains(response, "Итоговая сумма: 2000 руб.")
        self.assertNotContains(response, "скидка 10%")

    def test_different_products_discount_applied(self):
        response = self.client.post(self.url, {
            'person': 'Иван', 'address': 'Улица 1',
            f'product_{self.p1.id}': 1, f'product_{self.p2.id}': 1,
        })
        self.assertContains(response, "Итоговая сумма: 2700 руб.")
        self.assertContains(response, "Применена скидка 10%")
        self.assertEqual(Purchase.objects.count(), 2)
        
    def test_empty_cart_error(self):
        response = self.client.post(self.url, {
            'person': 'Иван', 'address': 'Улица 1',
            f'product_{self.p1.id}': 0, f'product_{self.p2.id}': 0,
        })
        self.assertContains(response, "Вы не выбрали ни одного товара")
        self.assertEqual(Purchase.objects.count(), 0) 

    def test_large_discount_order(self):
        response = self.client.post(self.url, {
            'person': 'Иван', 'address': 'Улица 1',
            f'product_{self.p1.id}': 5, f'product_{self.p2.id}': 2,
        })
        self.assertContains(response, "Итоговая сумма: 8100 руб.")
        self.assertContains(response, "Применена скидка 10%")
        self.assertEqual(Purchase.objects.count(), 7) 

    def test_checkout_get_method(self):
        response = self.client.get(self.url)
        self.assertContains(response, "Ошибка: неверный метод запроса.")