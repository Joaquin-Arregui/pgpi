from django.test import TestCase
from django.core.files import File
from django.urls import reverse
from .models import Category
from products.models import Product
from users.models import User
import os

class CategoryModelTest(TestCase):
    
    def setUp(self):
        self.product1 = Product.objects.create(title="Producto 1",description="Descripcion 1",price=20.0,stock=10,
            image='mario_sellado.png')
        self.product2 = Product.objects.create(title="Producto 2",description="Descripcion 2",price=35.0,stock=50,
            image='flash.png')

    def test_create_category(self):
        #test crear una categoria

        category = Category.objects.create(
            title="Categoria de prueba",
            description="Descripcion de prueba",
            image = 'mario_sellado.png'
        )

        self.assertEquals(category.title, "Categoria de prueba")
        self.assertEquals(category.description, "Descripcion de prueba")
        self.assertEqual(category.image.name, 'mario_sellado.png')
        self.assertIsNotNone(category.created_at)
        self.assertTrue(category.slug)
        
    def test_category_slug_generation(self):
        categoria1 = Category.objects.create(title="Titulo duplicado",description="Descripcion de prueba")
        categoria2 = Category.objects.create(title="Titulo duplicado",description="Descripcion de prueba 2")
        self.assertNotEqual(categoria1.slug,categoria2.slug)

    def test_cetegory_products(self):
        categoria = Category.objects.create(title="Titulo de prueba",description="Descripcion de prueba")
        categoria.products.add(self.product1,self.product2)

        self.assertEquals(categoria.products.count(), 2)
        self.assertIn(self.product1, categoria.products.all())
        self.assertIn(self.product2, categoria.products.all())

class CategoryViewTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(
            title="Categoria de prueba",
            description="Descripcion de prueba",
            image = ''
            #image = File(open('media/categories/mario_sellado.png', 'rb'))
        )
        self.staff_user = User.objects.create_user(username='staff', password='test123', is_staff=True)


    def test_category_list_view(self):
        response = self.client.get(reverse('categories:categories'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.category.title)
        self.assertContains(response, self.category.description)


    def test_category_detail_view(self):
        response = self.client.get(reverse('categories:category', args=[self.category.slug]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.category.title)


    def test_category_create_view(self):
        self.client.force_login(self.staff_user)
        response = self.client.post(reverse('categories:categories_create'), {
           'titulo': 'Nueva Categoría',
           'descripcion': 'Descripción de la nueva categoría'
        })

        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('categories:categories'))
        self.assertEqual(response.status_code, 200)

        new_category = Category.objects.get(title='Nueva Categoría')
        self.assertIsNotNone(new_category)
        self.assertEqual(new_category.description, 'Descripción de la nueva categoría')
   
    
    def test_category_update_view(self):
        self.client.force_login(self.staff_user)
        response = self.client.post(reverse('categories:categories_edit', args=[self.category.slug]), {
            'titulo': 'Categoria Actualizada',
            'descripcion': 'Nueva descripción',
        })

        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('categories:categories'), args=['categoria-actualizada'])
        self.assertEqual(response.status_code, 200)

        updated_category = Category.objects.get(pk=self.category.pk)
        self.assertEqual(updated_category.title, 'Categoria Actualizada')
        self.assertEqual(updated_category.description, 'Nueva descripción')

    
    def test_category_delete_view(self):
        self.client.force_login(self.staff_user)
        response = self.client.post(reverse('categories:categories_delete', args=[self.category.slug]))

        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('categories:categories'))
        self.assertEqual(response.status_code, 200)
        

        with self.assertRaises(Category.DoesNotExist):
            deleted_category = Category.objects.get(pk=self.category.pk)
     