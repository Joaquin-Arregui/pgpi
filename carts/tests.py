import decimal
from django.test import TestCase
from .models import Cart, Product, User
from django.db import transaction

class CartTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='user', password='pass')
        self.product = Product.objects.create(title='Test Product', price=10.00, stock=1)
        self.productExpensive = Product.objects.create(title='Test Expensive Product', price=50.00, stock=1)

    def test_create_new_cart(self):
        cart = Cart.objects.create(user=self.user)
        self.assertIsNotNone(cart.cart_id)

    def test_add_product_to_cart(self):
        cart = Cart.objects.create(user=self.user)
        response = self.client.post(f"/cart/agregar?quantity=1&product_id={self.product.id}")
        self.assertEqual(response.status_code, 302)


    def test_remove_product_from_cart(self):
        self.client.login(username='user', password='pass')
        cart = Cart.objects.create(user=self.user)
        response = self.client.post(f"/cart/agregar?quantity=1&product_id={self.product.id}")
        response = self.client.post(f"/cart/eliminar?product_id={self.product.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(cart.products.count(), 0)

    def test_update_cart_subtotal(self):
        cart = Cart.objects.create(user=self.user)
        cart.products.add(self.product)
        self.assertEqual(cart.subtotal, 10.00)
        cart.products.remove(self.product)
        self.assertEqual(cart.subtotal, 0.00)

    def test_update_cart_total(self):
        cart = Cart.objects.create(user=self.user)
        cart.products.add(self.product)
        self.assertEqual(cart.total, decimal.Decimal('14.99'))
        cart.products.remove(self.product)
        self.assertEqual(cart.total, 0.00)

    def test_cart_shipping_cost(self):
        cart = Cart.objects.create(user=self.user)
        cart.products.add(self.product)
        self.assertEqual(cart.shipping_cost(), 4.99)
        cart.products.add(self.productExpensive)
        self.assertEqual(cart.shipping_cost(), 0)


