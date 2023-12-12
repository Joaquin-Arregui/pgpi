from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('',views.ProductListView.as_view() , name="products"),
    path('search',views.ProductSearchListView.as_view() , name="search"),
    path('filter',views.ProductFilterListView.as_view() , name="filter"),
    path('<slug:slug>',views.ProductDetailView.as_view() , name="product"),
    path('<slug:slug>/delete',views.ProductDeleteView , name="product_delete"),
    path('<slug:slug>/edit',views.ProductEditView , name="product_edit"),
    path('create/', views.ProductCreateView, name='product_create'),

]
