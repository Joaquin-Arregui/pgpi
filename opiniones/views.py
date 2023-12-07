from django.shortcuts import render, redirect
from .models import Opinion

# Create your views here.

def opiniones(request):
    opiniones = Opinion.objects.all()
    if request.method == 'POST':
        user = request.user if request.user.is_authenticated else None
        nota = request.POST.get('nota')
        desc = request.POST.get('desc') if request.POST.get('desc') else 'No se ha añadido'
        opinion = Opinion.objects.create(user=user, nota=nota, desc=desc)
        opinion.save()
        return redirect('/opiniones')

    return render(request, 'opiniones.html', {
        'opiniones': opiniones
    })

def remove(request):
    id = request.GET.get('id')
    opinion = Opinion.objects.get(pk=id)
    Opinion.delete(opinion)
    return redirect('/opiniones')