from django.shortcuts import render
from products.models import Product
from django.shortcuts import redirect, get_object_or_404
from .models import Cart 
from .utils import get_or_create_cart
from .models import CartProducts
from django.shortcuts import HttpResponse





def cart(request):
    cart = get_or_create_cart(request)

    return render(request, 'carts/cart.html', {

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
            
  
            cart.products.remove(cart_product.product)
            

            product = cart_product.product
            product.stock += quantity
            product.save()

            return redirect('carts:cart')
        except CartProducts.DoesNotExist:
            return HttpResponse("Producto no encontrado en el carrito")
    else:
        return HttpResponse("Método no permitido")
def update_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        new_quantity = int(request.POST.get('quantity', 1))

        cart = get_or_create_cart(request)
        product = get_object_or_404(Product, pk=product_id)

        try:
            cart_product = CartProducts.objects.get(cart=cart, product=product)
            current_quantity = cart_product.quantity

            
            if new_quantity != current_quantity and 1 <= new_quantity <= product.stock:

                cart_product.update_quantity(new_quantity)

 
                updated_stock = product.stock + current_quantity - new_quantity
                product.stock = updated_stock
                product.save()
        except CartProducts.DoesNotExist:

            pass

   
        return redirect('carts:cart')
    else:

        pass