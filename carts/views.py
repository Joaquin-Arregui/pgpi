from django.shortcuts import render
from products.models import Product
from django.shortcuts import redirect, get_object_or_404
from .models import Cart 
from .utils import get_or_create_cart
from .models import CartProducts

# Create your views here.

def cart(request):
    cart = get_or_create_cart(request)

    return render(request, 'carts/cart.html', {
        #mandando el objeto cart al template
        'cart':cart
    })

def add(request):
    cart = get_or_create_cart(request)
    quantity = int(request.GET.get('quantity'))
    product_id = request.GET.get('product_id')
    product = get_object_or_404(Product, pk=product_id)

    if quantity < 0:
        return
    elif quantity > product.stock:
        return
    # si esa llave no existe, el valor de la llave será uno por default de productos
    new_stock = product.stock-quantity
    product.stock = new_stock
    product.save()
    cart_product = CartProducts.objects.create_or_update_quantity(cart=cart, product=product, quantity=quantity)
    #esta forma de agregar no esta BIEN PORQUE CADA VEZ QUE AGREGO NUEVOS NO SE ACTUALIZA, SOLO LOS QUE ENVIE EN EL MOMENTO
    #cart.products.add(product, through_defaults={
    #    'quantity': quantity
    #    
    #})
    #'product_id' es el nombre del formulario html donde obtiene el id del producto
    product = Product.objects.get(pk=product_id)
    #cart es una instacia del modelo por lo que para acceder a atributo products es la relacion ManytoMany
    cart.products.add(product)

    return render(request, 'carts/add.html', {
        'quantity': quantity,
        'product': product,
        'cp': cart_product
    })

def remove(request):
    cart = get_or_create_cart(request)
    product_id = request.POST.get('product_id')
    product = get_object_or_404(Product, pk=product_id)
    #'product_id' es el nombre del formulario html donde obtiene el id del producto
    product = Product.objects.get(pk=request.POST.get('product_id'))
    #cart es una instacia del modelo por lo que para acceder a atributo products es la relacion ManytoMany
    cart_product = cart.products
    ##quantity = cart_product.quantity
    cart.products.remove(product)
    ##new_stock = product.stock + quantity
    ##product.stock = new_stock
    ##product.save()
    return redirect('carts:cart')

def prueba(request, slug):
    cart = get_or_create_cart(request)
    product = get_object_or_404(Product, pk=request.POST.get('product_id'))
    #'product_id' es el nombre del formulario html donde obtiene el id del producto
    product = Product.objects.get(pk=request.POST.get('product_id'))
    #cart es una instacia del modelo por lo que para acceder a atributo products es la relacion ManytoMany
    cart.products.remove(product)

    return redirect('carts:cart')