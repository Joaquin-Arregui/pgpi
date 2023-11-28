from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.order, name='order'),
    path('envio/<slug:slug>/', views.envio, name="envio" ),
    path('seguimiento',views.seguimiento, name='seguimiento'),
    path('estado', views.estado, name='estado'),
    path('pago/<slug:slug>/', views.pago, name='pago' )
    
]