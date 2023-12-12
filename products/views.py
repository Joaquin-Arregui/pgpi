from django.shortcuts import render, redirect, get_object_or_404
from carts.utils import get_or_create_cart
from django.views.generic.list import ListView

from users.models import Admin
from .models import Product, Producer
from django.views.generic.detail import DetailView
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test


class ProductListView(ListView):
    paginate_by=5
    template_name = 'index.html'
    queryset = Product.objects.all().order_by('-id')

    def get_context_data(self, **kwargs):
        producers = Producer.objects.all()
        context = super().get_context_data(**kwargs)
        cart = get_or_create_cart(self.request)
        context['producers'] = producers
        context['cart'] = cart
        context['message'] = 'Listado de Productos'
        context['products'] = context['object_list'] 
        return context
    
class EscaparateView(ListView):
    paginate_by=5
    template_name = 'escaparate.html'
    queryset = Product.objects.exclude(stock=0).order_by('stock')[:3]

    def get_context_data(self, **kwargs):
        producers = Producer.objects.all()
        context = super().get_context_data(**kwargs)
        cart = get_or_create_cart(self.request)
        context['producers'] = producers
        context['cart'] = cart
        context['message'] = 'Listado de Productos'
        context['products'] = context['object_list'] 
        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = 'product.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = get_or_create_cart(self.request)
        context['cart'] = cart
        return context

@login_required
@user_passes_test(Admin.get_user_permissions)
def ProductDeleteView(request, slug):
    producto = Product.objects.filter(slug=slug).first()

    Product.delete(producto)

    return redirect('/')

@login_required
@user_passes_test(Admin.get_user_permissions)
def ProductCreateView(request):
    cart = get_or_create_cart(request)
    if request.method == 'POST':
        
        titulo = request.POST.get('titulo')
        descripcion = request.POST.get('descripcion')
        precio = request.POST.get('precio')
        stock = request.POST.get('stock')
        imagen = request.FILES.get('imagen')  

       
        product = Product(title=titulo, description=descripcion, price=precio, stock=stock, image=imagen)

       
        product.save()


        return redirect('/product/' + product.slug)

    return render(request, 'productCreate.html', {
        'cart': cart
    })

@login_required
@user_passes_test(Admin.get_user_permissions)
def ProductEditView(request, slug):
    product = Product.objects.filter(slug=slug).first()
    cart = get_or_create_cart(request)

    if request.method == 'POST':
     
        titulo = request.POST.get('titulo')
        descripcion = request.POST.get('descripcion')
        precio = request.POST.get('precio')
        stock = request.POST.get('stock')
        imagen = request.FILES.get('imagen')
     

        if titulo != None and titulo != '':
            product.title = titulo
        if descripcion != None and descripcion != '':
            product.description = descripcion
        if precio != None and precio != '':
            product.price = precio
        if stock != None and stock != '':
            product.stock = stock
        if imagen != None and imagen != '':
            product.image = imagen



        product.save()


        return redirect('/product/' + slug)

    return render(request, 'productEdit.html', {
        'product': product,
        'cart': cart
    })

class ProductSearchListView(ListView):
    template_name = 'searchResults.html'
    def get_queryset(self):
        filters = Q(title__icontains=self.query()) | Q(category__title__icontains=self.query())
        return Product.objects.filter(filters)

    def query(self):
        return self.request.GET.get('q')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = get_or_create_cart(self.request)
        producers = Producer.objects.all()
        context['producers'] = producers
        context['cart'] = cart
        context['query'] = self.query()
        context['count'] = context['object_list'].count()
        return context
    
class ProductFilterListView(ListView):
    template_name = 'filterResults.html'
    def get_queryset(self):
        min, max, producer = self.query()
        products = Product.objects.all()
        if not min=='':
            products = products.filter(price__gte=min)
        if not max=='':
            products = products.filter(price__lte=max)
        if not producer=='':
            products = products.filter(producer=producer)
        return products

    def query(self):
        min = self.request.GET.get('min')
        max = self.request.GET.get('max')
        producer = self.request.GET.get('producer')
        return min, max, producer

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        cart = get_or_create_cart(self.request)
        context['cart'] = cart
        min, max, producer = self.query()
        if min=='':
            min = 'No se ha establecido'
        context['min'] = min
        if max=='':
            max = 'No se ha establecido'
        context['max'] = max
        if producer=='':
            producer = 'No se ha establecido'
        else: 
            producer = get_object_or_404(Producer,pk=producer)
        context['producer'] = producer
        producers = Producer.objects.all()
        context['producers'] = producers
        context['count'] = context['object_list'].count()
        return context