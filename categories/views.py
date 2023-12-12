from django.shortcuts import render,redirect
from carts.utils import get_or_create_cart
from .models import Category
from django.views.generic.list import ListView
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from users.models import Admin

def categories(request):
    categories = Category.objects.all()
    cart = get_or_create_cart(request)
    return render(request, 'categories.html', {
        'object_list':categories,
        'cart': cart
    })

def category(request, slug):
    category = Category.objects.filter(slug=slug).first()
    products = category.products.all()
    cart = get_or_create_cart(request)

    return render(request, 'category.html', {
        'object_list':products,
        'category': category.title,
        'cart': cart
    })

@login_required
@user_passes_test(Admin.get_user_permissions)
def CategoryDeleteView(request, slug):
    category = Category.objects.filter(slug=slug).first()

    Category.delete(category)

    return redirect('/categories' )

@login_required
@user_passes_test(Admin.get_user_permissions)
def CategoryCreateView(request):
    cart = get_or_create_cart(request)

    if request.method == 'POST':

        titulo = request.POST.get('titulo')
        descripcion = request.POST.get('descripcion')
        imagen = request.FILES.get('imagen') 


        categoria = Category(title=titulo, description=descripcion, image=imagen)

        categoria.save()


        return redirect('/categories' )

    return render(request, 'categoryCreate.html', {
        'cart': cart
    })

@login_required
@user_passes_test(Admin.get_user_permissions)
def CategoryEditView(request, slug):
    category = Category.objects.filter(slug=slug).first()
    cart = get_or_create_cart(request)

    if request.method == 'POST':

        titulo = request.POST.get('titulo')
        descripcion = request.POST.get('descripcion')
        imagen = request.FILES.get('imagen')
        category.title = titulo
        category.description = descripcion
        category.image = imagen
        category.save()

        return redirect('/categories' )

    return render(request, 'categoryEdit.html', {
        'category': category,
        'cart': cart
    })
