from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth import authenticate
from .forms import RegisterForm
from products.models import Product
from users.models import User
from django.core.paginator import Paginator
from carts.utils import get_or_create_cart

def index(request):
    products = Product.objects.all().order_by('-id')
    paginator = Paginator(products, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    cart = get_or_create_cart(request)

    return render(request, 'index.html', {
        'cart': cart,
        'message': 'Listado de produtos',
        'title': 'Productos',
        'page_obj': page_obj,
        })

def info(request):
    cart = get_or_create_cart(request)
    return render(request, 'info.html', {
        'cart': cart

    })

def logout_view(request):
    logout(request)
    messages.success(request, 'Sesion cerrada exitosamente')
    return redirect('login')


def register(request):

    if request.user.is_authenticated:
        return redirect('index')

    form = RegisterForm(request.POST or None)
    
    if request.method == 'POST' and form.is_valid():
        user=User.objects.create(
            username=form.cleaned_data["username"],
            first_name= form.cleaned_data["first_name"],
            last_name= form.cleaned_data["last_name"],
            email= form.cleaned_data["email"],
            password=form.cleaned_data["password"]
        )



        if user:
            login(request, user)
            return redirect('index')

    return render(request, 'users/register.html', {
        'form': form
    })

@csrf_protect
def login_view(request):

    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        username = request.POST.get('username') 
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        if not user:
            user = User.objects.filter(username=username, password=password).first()
        if not user:
            user=User.objects.filter(email=username,password=password).first()
        if user:
            login(request, user)
            messages.success(request, 'Bienvenido {}'.format(user.username))
            if request.GET.get('next'):
                return HttpResponseRedirect(request.GET['next'] )
            return redirect('index')
        else:
            messages.error(request, 'Usuario o contraseña no validos')
    return render(request, 'users/login.html', {

    })


