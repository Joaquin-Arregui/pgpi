from django.db import models

from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):

    def get_full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

class Admin(User):
    @staticmethod
    def get_user_permissions(user):
        return user.is_staff and user.is_authenticated

class Customer(User):

    class Meta:
        proxy = True
        
    def get_productos(sef):
        return []



class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete = models.CASCADE)
    bio = models.TextField()
