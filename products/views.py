from django.shortcuts import render, redirect, get_object_or_404
from carts.utils import get_or_create_cart
from django.views.generic.list import ListView

from users.models import Admin
from .models import Product, Producer
from django.views.generic.detail import DetailView
#la clase q permite una consulta con diferentes filtros
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

class ProductDetailView(DetailView):
    model = Product
    template_name = 'product.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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
    if request.method == 'POST':
        # get data from the form
        titulo = request.POST.get('titulo')
        descripcion = request.POST.get('descripcion')
        precio = request.POST.get('precio')
        stock = request.POST.get('stock')
        imagen = request.FILES.get('imagen')  # get the image as an uploaded file

        # create a new product
        product = Product(title=titulo, description=descripcion, price=precio, stock=stock, image=imagen)

        # save the product
        product.save()

        # redirect to the product page after saving
        return redirect('/product/' + product.slug)

    return render(request, 'productCreate.html')

@login_required
@user_passes_test(Admin.get_user_permissions)
def ProductEditView(request, slug):
    product = Product.objects.filter(slug=slug).first()

    if request.method == 'POST':
        # get data from the form
        titulo = request.POST.get('titulo')
        descripcion = request.POST.get('descripcion')
        precio = request.POST.get('precio')
        stock = request.POST.get('stock')
        imagen = request.FILES.get('imagen')
        # add other fields as necessary

        # update the product
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
        # update other fields as necessary

        # save the product
        product.save()

        # redirect to the same page after saving
        return redirect('/product/' + slug)

    return render(request, 'productEdit.html', {
        'product': product
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
            producer = get_object_or_404(Producer,pk=producer).title
        context['producer'] = producer
        context['count'] = context['object_list'].count()
        return context
    

def comentar(request):
    slug= request.GET.get('product_id')
    comentario= request.GET.get('comment')
    product = get_object_or_404(Product, pk=slug)
    user = request.user.get_full_name()
    product.comments[user] = comentario
    product.save()
    return redirect('/product/'+product.slug)