from django.shortcuts import render,redirect
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

def CategoryDeleteView(request, slug):
    category = Category.objects.filter(slug=slug).first()

    Category.delete(category)

    return redirect('/categories' )

def CategoryCreateView(request):

    if request.method == 'POST':
        # get data from the form
        titulo = request.POST.get('titulo')
        descripcion = request.POST.get('descripcion')
        imagen = request.FILES.get('imagen')  # get the image as an uploaded file

        # create a new product
        categoria = Category(title=titulo, description=descripcion, image=imagen)

        # save the product
        categoria.save()

        # redirect to the product page after saving
        return redirect('/categories' )

    return render(request, 'categoryCreate.html')

def CategoryEditView(request, slug):
    category = Category.objects.filter(slug=slug).first()

    if request.method == 'POST':
        # get data from the form
        titulo = request.POST.get('titulo')
        descripcion = request.POST.get('descripcion')
        imagen = request.FILES.get('imagen')
        # add other fields as necessary

        # update the category
        category.title = titulo
        category.description = descripcion
        category.image = imagen
        # update other fields as necessary

        # save the category
        category.save()

        # redirect to the same page after saving
        return redirect('/categories' )

    return render(request, 'categoryEdit.html', {
        'category': category
    })
