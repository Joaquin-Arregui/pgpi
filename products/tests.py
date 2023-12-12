import decimal
from django.test import TestCase
from .models import Product

from users.models import User
from django.urls import reverse



class ProductModelTest(TestCase):
    def setUp(self):
        """
        Método para configurar los objetos de prueba antes de cada test.
        """
        self.product = Product.objects.create(
            title='Test Product',
            description='Test description',
            price=9.99,
            stock=100
        )

    def test_product_creation(self):
        """
        Prueba que se crea correctamente un producto.
        """
        self.assertEqual(self.product.title, 'Test Product')
        self.assertEqual(self.product.description, 'Test description')
        self.assertEqual(self.product.price, 9.99)
        self.assertEqual(self.product.stock, 100)

    def test_product_str(self):
        """
        Prueba el método __str__ del modelo Product.
        """
        self.assertEqual(str(self.product), 'Test Product')

class ProductEditViewTest(TestCase):
    def setUp(self):
        """
        Método para configurar los objetos de prueba antes de cada test.
        """
        self.product = Product.objects.create(
            title='Test Product',
            description='Test description',
            price=9.99,
            stock=100
        )
        self.product_data = {
            'titulo': 'Updated Product',
            'descripcion': 'Updated description',
            'precio': 19.99,
            'stock': 200
        }

    def test_product_edit(self):
        """
        Prueba que se edita correctamente un producto a través de la vista.
        """
        response = self.client.post(f'/product/{self.product.slug}/edit', self.product_data)
        self.assertEqual(response.status_code, 302) 
        self.product.refresh_from_db()
        self.assertEqual(self.product.title, 'Updated Product')
        self.assertEqual(self.product.description, 'Updated description')
        self.assertEqual(self.product.price, decimal.Decimal( "19.99"))
        self.assertEqual(self.product.stock, 200)

class ProductDeleteViewTest(TestCase):
    def setUp(self):
        """
        Método para configurar los objetos de prueba antes de cada test.
        """
        self.staff_user = User.objects.create_user(username='staff', password='test123', is_staff=True)
        self.non_staff_user = User.objects.create_user(username='non_staff', password='test123', is_staff=False)
        self.product = Product.objects.create(
            title='Test Product',
            description='Test description',
            price=9.99,
            stock=100
        )

    def test_product_delete_staff(self):
        """
        Prueba que un usuario con is_staff=True puede eliminar un producto.
        """
        self.client.force_login(self.staff_user)
        response = self.client.post(reverse('products:product_delete', kwargs={'slug': self.product.slug}))
        self.assertEqual(response.status_code, 302) 
        self.assertEqual(Product.objects.count(), 0)

    def test_product_delete_non_staff(self):
        """
        Prueba que un usuario sin is_staff=True no puede eliminar un producto.
        """
        self.client.force_login(self.non_staff_user)
        response = self.client.post(reverse('products:product_delete', kwargs={'slug': self.product.slug}))
        self.assertEqual(Product.objects.count(), 1)  

class ProductEditViewTest(TestCase):
    def setUp(self):
        """
        Método para configurar los objetos de prueba antes de cada test.
        """
        self.staff_user = User.objects.create_user(username='staff', password='test123', is_staff=True)
        self.non_staff_user = User.objects.create_user(username='non_staff', password='test123', is_staff=False)
        self.product = Product.objects.create(
            title='Test Product',
            description='Test description',
            price=9.99,
            stock=100
        )
        self.product_data = {
            'titulo': 'Updated Product',
            'descripcion': 'Updated description',
            'precio': 19.99,
            'stock': 200
        }

    def test_product_edit_staff(self):
        """
        Prueba que un usuario con is_staff=True puede editar un producto.
        """
        self.client.force_login(self.staff_user)
        response = self.client.post(reverse('products:product_edit', kwargs={'slug': self.product.slug}), self.product_data)
        self.assertEqual(response.status_code, 302)  
        self.product.refresh_from_db()
        self.assertEqual
