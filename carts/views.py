from django.shortcuts import render
from products.models import Product
from django.shortcuts import redirect, get_object_or_404
from .models import Cart 
from .utils import get_or_create_cart
from .models import CartProducts
from django.shortcuts import HttpResponse



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
    product = Product.objects.get(pk=product_id)
    cart.products.add(product)

    return redirect('/product/'+product.slug)

def remove(request):
    if request.method == 'POST':
        cart = get_or_create_cart(request)
        product_id = request.POST.get('product_id')
        
        try:
            cart_product = CartProducts.objects.get(cart=cart, product__id=product_id)
            quantity = cart_product.quantity
            
            # Elimina el producto del carrito
            cart.products.remove(cart_product.product)
            
            # Aumenta el stock del producto eliminado
            product = cart_product.product
            product.stock += quantity
            product.save()

            return redirect('carts:cart')
        except CartProducts.DoesNotExist:
            return HttpResponse("Producto no encontrado en el carrito")
    else:
        return HttpResponse("Método no permitido")

def prueba(request, slug):
    cart = get_or_create_cart(request)
    product = get_object_or_404(Product, pk=request.POST.get('product_id'))
    #'product_id' es el nombre del formulario html donde obtiene el id del producto
    product = Product.objects.get(pk=request.POST.get('product_id'))
    #cart es una instacia del modelo por lo que para acceder a atributo products es la relacion ManytoMany
    cart.products.remove(product)

    return redirect('carts:cart')

def update_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        new_quantity = int(request.POST.get('quantity', 1))

        cart = get_or_create_cart(request)
        product = get_object_or_404(Product, pk=product_id)

        try:
            cart_product = CartProducts.objects.get(cart=cart, product=product)
            current_quantity = cart_product.quantity

            # Verifica si la cantidad es diferente antes de actualizar
            if new_quantity != current_quantity and 1 <= new_quantity <= product.stock:
                # Actualiza la cantidad del producto en el carrito
                cart_product.update_quantity(new_quantity)

                # Actualiza el stock del producto
                updated_stock = product.stock + current_quantity - new_quantity
                product.stock = updated_stock
                product.save()
        except CartProducts.DoesNotExist:
            # Manejar el caso en que el producto no esté en el carrito
            pass

        # Redirige a la página del carrito
        return redirect('carts:cart')
    else:
        # Manejar el caso en que la solicitud no sea POST
        pass