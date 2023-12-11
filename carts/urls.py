from django.urls import path
from . import views

app_name = 'carts'

urlpatterns = [
    path('', views.cart, name='cart'),
    path('agregar', views.add, name='add'),
    path('eliminar', views.remove, name='remove'),
    path('update-cart/', views.update_cart, name='update_cart'),
]
