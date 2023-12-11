from django.test import TestCase
from django.urls import reverse
from .models import User, Perfil

class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser', first_name='Test', last_name='User')

    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.get_full_name(), 'Test User')

class UserViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser', first_name='Test', last_name='User')

    def test_perfil_view(self):
        response = self.client.get(reverse('users:user'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'perfil.html')

    def test_user_list_view(self):
        response = self.client.get(reverse('users:list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'listUsers.html')

    def test_user_edit_view(self):
        response = self.client.get(reverse('users:edit') + f'?slug={self.user.username}')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'userEdit.html')
        data = {
            'username': 'newusername',
            'first_name': 'New',
            'last_name': 'User',
        }
        response = self.client.post(reverse('users:edit') + f'?slug={self.user.username}', data)
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'newusername')

class UserDeleteViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser', first_name='Test', last_name='User')

    def test_user_delete_view(self):
        response = self.client.get(reverse('users:delete') + f'?slug={self.user.username}')
        self.assertEqual(response.status_code, 302)
        self.assertFalse(User.objects.filter(username='testuser').exists())