from django.shortcuts import render, redirect
# from django.views.generic import View
from .forms import CrearPaseadorCuidador
from .models import PaseadorCuidador
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def agregar_paseador_cuidador(request):
    if (request.user.is_superuser == False):
        return redirect("home")

    if request.method == "POST":
        form = CrearPaseadorCuidador(request.POST)
        if form.is_valid():
            PaseadorCuidador.objects.create(nomyap=request.POST['nomyap'], 
                                 dni=request.POST['dni'],
                                 textolibre=request.POST['textolibre'])
            return redirect('home')
    else:
        form = CrearPaseadorCuidador()
    return render(request, 'agregar_paseador_cuidador.html', {
        'form': form
    })

def listar_paseadores_cuidadores(request):
    paseadores_cuidadores = PaseadorCuidador.objects.all
    return render(request, "listar_paseadores_cuidadores.html", {
        'paseadores_cuidadores': paseadores_cuidadores
    })

