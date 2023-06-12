from django.shortcuts import render
from .models import Campaña
from .forms import CrearCampaña

# Create your views here.
def agregar_campaña(request):
    if request.method == "POST":
        form = CrearCampaña(request.POST)
        if form.is_valid():
            PaseadorCuidador.objects.create(nombre=request.POST['nombre'], 
                                 monto_objetivo=request.POST['monto_objetivo'],
                                 descripcion=request.POST['descripcion'])
            return redirect('home')
    else:
        form = CrearCampaña()
    return render(request, 'agregar_campaña.html', {
        'form': form
    })