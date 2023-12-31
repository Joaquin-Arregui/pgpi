# test.py

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from users.models import User
from carts.models import Cart
from .models import Order

# Pruebas para el modelo Order
class OrderModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser', password='testpassword')
        self.cart = Cart.objects.create(user=self.user)
        self.order = Order.objects.create(user=self.user, cart=self.cart)

    def test_update_total(self):
        """
        Prueba que el método update_total actualiza correctamente el total de la orden
        """
        self.order.update_total()
        self.assertEqual(self.order.total, self.order.get_total())

    def test_estado(self):
        """
        Prueba que el método estado devuelve el estado correcto de la orden
        """
        self.order.tarjeta = "1234567812345678"
        self.order.save()
        self.assertEqual(self.order.estado(), "En proceso")

# Pruebas para las vistas
class OrderViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.cart = Cart.objects.create(user=self.user)
        self.order = Order.objects.create(user=self.user, cart=self.cart)



    def test_envio_view(self):
        """
        Prueba que la vista 'envio' devuelve correctamente la orden especificada
        """
        response = self.client.get(reverse('orders:envio', args=[str(self.order.order_id)]))  # Cambia 'envio' a 'orders:envio'
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/id_envio.html')
        self.assertEqual(response.context['order'], self.order)
