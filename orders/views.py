from django.shortcuts import get_object_or_404, redirect, render
from carts.utils import get_or_create_cart
from .models import Order, Cart
from django.contrib.auth.decorators import login_required
from .utils import breadcrumb
from django.utils import timezone
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

def pago(request):
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

def SeguimientoDeleteView(request):
    order_id = request.GET.get('slug')
    order = Order.objects.filter(order_id=order_id).first()

    Order.delete(order)

    return redirect('/')

def SeguimientoEditView(request):
    order_id = request.GET.get('slug')
    order = Order.objects.filter(order_id=order_id).first()
    context = {'order': order}
    
    if request.method == 'POST' and not order.enviado:
        
        order.enviado  = timezone.now()
        
        # update other fields as necessary

        # save the product
        order.save()

        # redirect to the same page after saving
        return redirect('/order/edit?slug=' + order_id)
    
    if request.method == 'POST' and order.enviado:
        
        order.entregado = timezone.now()
        
        # update other fields as necessary

        # save the product
        order.save()

        # redirect to the same page after saving
        return redirect('/order/edit?slug=' + order_id)
    
    return render(request, 'orders/orderEdit.html', {
        'order': order
    })


