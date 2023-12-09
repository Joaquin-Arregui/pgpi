from django.shortcuts import get_object_or_404, redirect, render
from carts.utils import get_or_create_cart
from .models import Order, Cart
from django.contrib.auth.decorators import login_required
from .utils import breadcrumb
from django.views.generic.list import ListView
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail


@login_required(login_url='login')
def order(request):
    cart = get_or_create_cart(request)

    order = cart.order

    if order is None and request.user.is_authenticated:
        order = Order.objects.create(cart=cart, user=request.user)
    if order:
        request.session['order_id'] = order.order_id
    print('Este es cart de order', cart)
    return render(request, 'orders/order.html', {
        'cart': cart,
        'order': order,
        'breadcrumb': breadcrumb()
    })

def envio(request, slug):
    order = get_object_or_404(Order, order_id=slug)
    
    # Construir el contenido del correo con detalles de todos los productos
    cart_products = order.cart.products_related()

    # Construir el contenido del correo con detalles de todos los productos y cantidades
    email_content = f'Gracias por tu compra en nuestro sitio.\n\nDetalles de la compra:\n\n'
    for cart_product in cart_products:
        email_content += f"Producto: {cart_product.product.title}\n"
        email_content += f"Cantidad: {cart_product.quantity}\n"
        # Agrega otros detalles del producto según sea necesario

    email_content += f'Importe: {order.total}\nDirección de entrega: {order.calle} {order.numero}, {order.ciudad}, {order.codigopostal}'

    # Envío del correo
    send_mail(
        'Confirmación de compra',
        email_content,
        'collectaweb.pgpi@gmail.com',  # Reemplaza con tu dirección de correo electrónico
        [request.user.email],  # Reemplaza con el correo electrónico del usuario
        fail_silently=False,
    )
    context = {'order': order}
    return render(request, 'orders/id_envio.html', context)

def seguimiento(request):
   return render(request, 'orders/seguimiento.html')

def estado(request):
    order_id = request.GET.get('slug')
    order = get_object_or_404(Order, order_id=order_id)
    context = {'order': order}
    return render(request, 'orders/estadopedido.html', context)

def pago(request):
    id= request.GET.get("cart")
    cart = get_object_or_404(Cart, pk=id)
    pago=request.GET.get("pago")
    if pago=="tarjeta":
        pago=True
    else:
        pago=False
    envio=request.GET.get("envio")
    if not envio=="tienda":
        envio=True
    else:
        envio=False
    order=Order.objects.create(
    cart=cart,
    user=request.user if request.user.is_authenticated else None)
    context = {'order': order,
                'pago':pago,
                'envio':envio}
    if request.method == 'POST':

        nombre = request.POST.get('firstName')
        apellidos = request.POST.get('lastName')
        calle = request.POST.get('street')
        numero = request.POST.get('number')
        codigopostal = request.POST.get('postalCode')
        ciudad = request.POST.get('city')
        tarjeta = request.POST.get('cardNumber')
        cvv = request.POST.get('cvv') 
        fechacad = request.POST.get('expiryDate')      


        order.nombre=nombre
        order.apellidos=apellidos
        order.calle = calle
        order.numero = numero
        order.codigopostal=codigopostal
        order.ciudad=ciudad
        order.tarjeta=tarjeta
        order.cvv=cvv
        order.fechacad=fechacad


        order.save()


        return redirect('/order/envio/' + order.order_id)
    return render(request, 'orders/pasarelapago.html', context)

def pagocontrareembolso(request):
    id= request.GET.get("cart")
    cart = get_object_or_404(Cart, pk=id)
    order=Order.objects.create(
    cart=cart,
    user=request.user if request.user.is_authenticated else None)
    context = {'order': order}
    if request.method == 'POST':

        nombre = request.POST.get('firstName')
        apellidos = request.POST.get('lastName')
        calle = request.POST.get('street')
        numero = request.POST.get('number')
        codigopostal = request.POST.get('postalCode')
        ciudad = request.POST.get('city')    


        order.nombre=nombre
        order.apellidos=apellidos
        order.calle = calle
        order.numero = numero
        order.codigopostal=codigopostal
        order.ciudad=ciudad


        order.save()


        return redirect('/order/envio/' + order.order_id)
    return render(request, 'orders/pagocontrareembolso.html', context)


def SeguimientoDeleteView(request):
    order_id = request.GET.get('slug')
    order = Order.objects.filter(order_id=order_id).first()

    Order.delete(order)

    return redirect('/')

def SeguimientoListView(request):
    orders = Order.objects.all().order_by('-id')
    context = {
        'message': 'Listado de Productos',
        'orders': orders,
    }
    return render(request, 'orders/listOrders.html', context)
    #orders = Order.objects.all().order_by('-id')
    #return render(request, 'orders/listOrders.html', {'orders': orders})

def SeguimientoEditView(request):
    order_id = request.GET.get('slug')
    order = Order.objects.filter(order_id=order_id).first()
    context = {'order': order}
    
    if request.method == 'POST' and not order.enviado:
        
        order.enviado  = timezone.now()
        


        order.save()

        return redirect('/order/edit?slug=' + order_id)
    
    if request.method == 'POST' and order.enviado:
        
        order.entregado = timezone.now()
        



        order.save()


        return redirect('/order/edit?slug=' + order_id)
    
    return render(request, 'orders/orderEdit.html', {
        'order': order
    })


