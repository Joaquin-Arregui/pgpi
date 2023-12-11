from django.shortcuts import render, redirect
from .models import Opinion
from users.models import Admin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone

# Create your views here.

@login_required(login_url='login')
def opiniones(request): 
    opiniones = Opinion.objects.all()
    if request.method == 'POST':
        user = request.user
        nota = request.POST.get('nota')
        desc = request.POST.get('desc') if request.POST.get('desc') else 'No se ha añadido'
        opinion = Opinion.objects.create(user=user, nota=nota, desc=desc)
        opinion.save()
        return redirect('/opiniones')

    return render(request, 'opiniones.html', {
        'opiniones': opiniones
    })

@login_required(login_url='login')
@user_passes_test(Admin.get_user_permissions)
def procesar(request):
    id = request.GET.get('id')
    opinion = Opinion.objects.get(pk=id)
    if opinion.inicio_procesado == None:
        opinion.inicio_procesado = timezone.now()
    elif opinion.fin_procesado == None:
        opinion.fin_procesado = timezone.now()
    opinion.save()
    return redirect('/opiniones')