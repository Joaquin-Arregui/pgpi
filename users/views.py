from django.shortcuts import render,redirect
from django.views.generic.detail import DetailView
from .models import User
from carts.utils import get_or_create_cart

def perfil(request):
    cart = get_or_create_cart(request)
    if request.method == 'POST':
        user=request.user
        nombre = request.POST.get('firstName')
        apellidos = request.POST.get('lastName')
        correo = request.POST.get('email')
        calle = request.POST.get('street')
        numero = request.POST.get('number')
        codigopostal = request.POST.get('postalCode')
        ciudad = request.POST.get('city')
        tarjeta = request.POST.get('cardNumber')
        cvv = request.POST.get('cvv') 
        fechacad = request.POST.get('expiryDate')      

        user.first_name=nombre
        user.last_name=apellidos
        user.email=correo
        user.calle = calle
        user.numero = numero
        user.codigopostal=codigopostal
        user.ciudad=ciudad
        user.tarjeta=tarjeta
        user.cvv=cvv
        user.fechacad=fechacad

        user.save()

    return render(request, 'perfil.html', {
        'cart': cart
    })

class perfilDetalle(DetailView):
    model = perfil
    template_name = 'perfil.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = get_or_create_cart(self.request)
        context['cart'] = cart
        return context

def UserDeleteView(request):
    username = request.GET.get('slug')
    user = User.objects.filter(username=username).first()

    User.delete(user)

    return redirect('/users/list')

def UserListView(request):
    users = User.objects.all().order_by('-id')
    context = {
        'message': 'Listado de Productos',
        'users': users,
    }
    return render(request, 'listUsers.html', context)
    #orders = Order.objects.all().order_by('-id')
    #return render(request, 'orders/listOrders.html', {'orders': orders})

def UserEditView(request):
    username = request.GET.get('slug')
    user = User.objects.filter(username=username).first()
    context = {'user': user}
    
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        user.username = username
        user.first_name = first_name
        user.last_name = last_name

        user.save()
        return redirect('/users/edit?slug=' + username)
    
    return render(request, 'userEdit.html', {
        'user': user
    })
