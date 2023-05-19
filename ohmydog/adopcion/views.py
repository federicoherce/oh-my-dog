from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import PublicarPerroEnAdopcion
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required
def publicar(request):
    if request.method == "POST":  
        form = PublicarPerroEnAdopcion(request.POST)
        if form.is_valid():
            adopcion = form.save(commit=False)
            adopcion.publicado_por = request.user
            adopcion.save()
            messages.success(request, 'Perro publicado con exito')
            return redirect('perros_en_adopcion')
        else:
            return render(request, "publicar_perro.html", {"form": form})
    else:  
        form = PublicarPerroEnAdopcion()
        return render(request, "publicar_perro.html", {"form": form})


def listado(request):
    return render(request, "perros_en_adopcion.html")