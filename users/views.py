from django.shortcuts import render
from django.views.generic.detail import DetailView

def perfil(request):
    return render(request, 'perfil.html')

class perfilDetalle(DetailView):
    model = perfil
    template_name = 'perfil.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #print(context)
        return context