from django.urls import path
from . import views

app_name = 'categories'

urlpatterns = [
    path('<slug:slug>',views.category , name="category"),
    path('', views.categories, name='categories'),
    path('create/', views.CategoryCreateView, name='categories_create'),
    path('<slug:slug>/delete',views.CategoryDeleteView , name="categories_delete"),
    path('<slug:slug>/edit',views.CategoryEditView , name="categories_edit"),
]