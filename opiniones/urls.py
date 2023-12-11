from django.urls import path
from . import views

app_name = 'opiniones'

urlpatterns = [
    path('', views.opiniones, name='opiniones'),
    path('process', views.procesar, name='process'),
]
