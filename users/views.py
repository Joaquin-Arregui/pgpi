from django.shortcuts import render,redirect
from django.views.generic.detail import DetailView
from .models import User

def perfil(request):
    return render(request, 'perfil.html')

class perfilDetalle(DetailView):
    model = perfil
    template_name = 'perfil.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #print(context)
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