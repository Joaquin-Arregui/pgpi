
from django.db import models
from users.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Opinion(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    nota = models.SmallIntegerField(default=5, validators=[MinValueValidator(1), MaxValueValidator(5)])
    desc = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    inicio_procesado = models.DateTimeField(null=True,blank=True)
    fin_procesado = models.DateTimeField(null=True,blank=True)

    def estado(self):
        res = 'Sin procesar'
        if self.inicio_procesado!=None:
            res= "En proceso"

            if self.fin_procesado != None:
                res= "Proceso completado"
        return res
