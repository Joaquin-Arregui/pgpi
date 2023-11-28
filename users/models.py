from django.db import models

from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):

    def get_nombre_completo(self):
        return '{}-{}'.format(self.first_name, self.last_name)

class Admin(User):

    def get_user_permissions( obj: User | None = ...):
        return User.is_staff

class Customer(User):

    class Meta:
        proxy = True
        
    def get_productos(sef):
        return []



class Profile(models.Model):
    usuario = models.OneToOneField(User, on_delete = models.CASCADE)
    bio = models.TextField()
