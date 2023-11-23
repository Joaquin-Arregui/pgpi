from django.shortcuts import render
from carts.utils import get_or_create_cart
from .models import Category
from django.views.generic.list import ListView

def categories(request):
    categories = Category.objects.all()
    return render(request, 'categories.html', {
        'object_list':categories
    })

def category(request, slug):
    category = Category.objects.filter(slug=slug).first()
    products = category.products.all()

    return render(request, 'category.html', {
        'object_list':products,
        'category': category.title
    })