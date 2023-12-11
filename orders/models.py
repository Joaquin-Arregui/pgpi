import uuid
from enum import Enum
from django.db import models
from users.models import User
from carts.models import Cart
from django.db.models.signals import pre_save




class Order(models.Model):
    order_id = models.CharField(max_length=100, null=False, blank=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    correo = models.EmailField(blank=True)
    shipping_total = models.DecimalField(default=5, max_digits=8, decimal_places=2)
    subtotal = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    total = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    enviado= models.DateField(null=True, blank=True)
    entregado=models.DateField(null=True,blank=True)
    nombre = models.CharField(max_length=40, null=True, blank=False, unique=False)
    apellidos = models.CharField(max_length=40, null=True, blank=False, unique=False)
    calle = models.CharField(max_length=40, null=True, blank=False, unique=False)
    numero = models.IntegerField(null=True, blank=False, unique=False)
    codigopostal = models.IntegerField(null=True, blank=False, unique=False)
    ciudad = models.CharField(max_length=40, null=True, blank=False, unique=False)
    tarjeta = models.CharField(max_length=16, null=True, blank=True)
    cvv = models.CharField(max_length=3, null=True, blank=True)
    fechacad = models.CharField(max_length=5, null=True, blank=True)



    def __str__(self):
        return self.order_id

    def get_total(self):
        return self.cart.total

    def update_total(self):
        self.total = self.get_total()
        self.save()

    def estado(self):

        res= "En proceso"

        if self.enviado != None:
            if self.entregado !=None:
                res= "Entregado"
            else:
                res= "Enviado"
        return res
        

def set_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = str(uuid.uuid4())


def set_total(sender, instance, *args, **kwargs):
    instance.total = instance.get_total()

pre_save.connect(set_order_id, sender=Order)
pre_save.connect(set_total, sender=Order)