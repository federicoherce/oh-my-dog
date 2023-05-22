from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import PublicarPerroEnAdopcion
from .models import Adopcion
from autenticacion.models import CustomUser
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from autenticacion.models import CustomUser
from django.core.mail import send_mail


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



def listar_perros_adopcion(request):
    perros_en_adopcion = Adopcion.objects.all

    if request.method == "POST":
        #perro_a_borrar = Adopcion.objects.get(nombre=request.POST['perros_adopcion.'])
        #perro_a_borrar.delete()
        redirect("perros_en_adopcion")

    return render(request, "perros_en_adopcion.html", {
        'perros_en_adopcion': perros_en_adopcion
    })

def marcar_Adoptado(request, perro_id):
    perroAdoptado = Adopcion.objects.get(id=perro_id)

    if request.method == 'POST':
        perroAdoptado.adoptado = not perroAdoptado.adoptado
        perroAdoptado.save()

    return redirect('perros_en_adopcion')

def eliminar_perro_en_adopcion(request, perro_id):
    perro = Adopcion.objects.get(id=perro_id)

    if request.method == 'POST':
        perro.delete()
    
    return redirect('perros_en_adopcion')

def enviar_solicitud_adopcion(request, autor, interesado, perro):
    publicado_por = CustomUser.objects.get(id=autor)
    quiere_adoptar = CustomUser.objects.get(id=interesado)
    
    asunto_interesado = "Solicitud enviada"
    msj_interesado = "Su solicitud de adopcion fue enviada con exito, espere a que el dueño se ponga en contacto con usted para concretar la adopcion de " + perro
    send_mail(asunto_interesado, msj_interesado, 'ohmydogg.vet@gmail.com', [quiere_adoptar.email])
    
    asunto_autor = "Alguien quiere adoptar a tu perro"
    msj_autor = quiere_adoptar.email + " ha solicitado adoptar a " + perro + ". Comuníquese con el para concretar su adopción"
    send_mail(asunto_autor, msj_autor, "ohmydogg.vet@gmail.com", [publicado_por.email])
    messages.success(request, 'Solicitud enviada')
    return redirect('perros_en_adopcion')