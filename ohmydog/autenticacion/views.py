from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from .forms import CustomUserCreationForm, EmailAuthenticationForm, CambiarEmailForm
from .models import CustomUser
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required

# Create your views here.


class registro(View):
    
    def get(self, request):
        form = CustomUserCreationForm()
        
        return render(request, 'registro.html', {"form": form})
    
    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            msj = 'Gracias por registrarse en Oh My Dog, su contraseña es: ' + password
            send_mail('Registro Oh My Dog', msj, 'ohmydogg.vet@gmail.com', [email])
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
            user = CustomUser.objects.get(email = nombre_usuario)
            if usuario is not None:
                login(request, usuario)
                if user.get_activo():
                    return redirect('home')
                else:
                    return redirect('cambiarContra')
        else:
            messages.error(request, "información incorrecta")
    form=EmailAuthenticationForm()
    return render(request, "login.html", {"form": form}) 

@login_required      
def cambiarContra(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user) # no cierra sesion
            user = CustomUser.objects.get(email = request.user)
            user.activo = True
            user.save()
            return redirect("/")
    else:
        form = PasswordChangeForm(request.user)
    return render(request, "cambiarContra.html", {"form": form})

@login_required
def cambiarEmail(request):
    mensaje_error = ' '
    formulario = CambiarEmailForm()
    if request.method == 'POST':
        formulario = CambiarEmailForm(data=request.POST)
        if formulario.is_valid():
            nuevoEmail = request.POST.get('email')
            todosLosEmails = CustomUser.objects.values_list('email', flat=True)
            if nuevoEmail not in todosLosEmails:
                user = CustomUser.objects.get(email = request.user)
                user.email = nuevoEmail
                user.save()
                return redirect('/')
            else:
                messages.error(request, "Ese email ya se encuentra registrado")
    return render(request, 'cambiarEmail.html', {"form": formulario})
