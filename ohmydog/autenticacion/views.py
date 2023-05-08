from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import CustomUserCreationForm
from .forms import EmailAuthenticationForm

# Create your views here.


class registro(View):
    
    def get(self, request):
        form = CustomUserCreationForm()
        
        return render(request, 'registro.html', {"form": form})
    
    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            return redirect('agregar_perro')
        else:
            return render(request, "registro.html", {"form": form})
    
def cerrar_sesion(request):
    logout(request)
    return redirect('home')

def loguear(request):
        if request.method=="POST":
            form = EmailAuthenticationForm(request, data=request.POST)
            if form.is_valid():
                nombre_usuario=form.cleaned_data.get("username")
                contra=form.cleaned_data.get("password")
                usuario=authenticate(username=nombre_usuario, password=contra)
                if usuario is not None:
                    login(request, usuario)
                    return redirect('home')
                else:
                    messages.error(request, "usuario no válido")
            else:
                messages.error(request, "información incorrecta")
        form=EmailAuthenticationForm()
        return render(request, "login.html", {"form": form}) 
        