from django.urls import path
from . import views

app_name = 'categories'

urlpatterns = [
    path('<slug:slug>',views.category , name="category"),
    path('', views.categories, name='categories'),
]