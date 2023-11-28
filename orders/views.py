from django.shortcuts import get_object_or_404, redirect, render
from carts.utils import get_or_create_cart
from .models import Order
from django.contrib.auth.decorators import login_required
from .utils import breadcrumb
# Create your views here.

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
    context = {'order': order}
    return render(request, 'orders/id_envio.html', context)

def seguimiento(request):
   return render(request, 'orders/seguimiento.html')

def estado(request):
    order_id = request.GET.get('slug')
    order = get_object_or_404(Order, order_id=order_id)
    context = {'order': order}
    return render(request, 'orders/estadopedido.html', context)

def pago(request,slug):
    order = get_object_or_404(Order, order_id=slug)
    context = {'order': order}
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

