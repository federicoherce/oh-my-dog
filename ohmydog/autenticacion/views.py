from typing import Any, Dict, Mapping, Optional, Type, Union
from django.db.models.query import QuerySet
from django.forms.utils import ErrorList
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.views.generic import View
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib import messages
from .forms import CustomUserCreationForm, EmailAuthenticationForm, FiltrosDeListadoDeClientes, CambiarEmailForm, modificarDatosCliente, ModificarDatosPerro
from django.contrib.auth.decorators import login_required, user_passes_test
from perros.models import Perro, LibretaSanitaria, Vacuna
from django.views.generic import ListView, DetailView
from .models import CustomUser
from django.contrib.auth.forms import PasswordChangeForm
from django.core.mail import send_mail
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from io import BytesIO
from django.utils import timezone
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors

# Create your views here.

def is_superuser(user):
    return user.is_superuser

@login_required(login_url='login')
@user_passes_test(is_superuser, login_url='home')
def registro(request):
    
    password = CustomUser.objects.make_random_password(length=5, 
    allowed_chars='abcdefghijkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ0123456789')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            password = form.cleaned_data['password1']
            return redirect('agregar_perro', form.cleaned_data['dni'], password)
        else:
            return render(request, "registro.html", {"form": form, "contra": password})
    else:
        form = CustomUserCreationForm()
        return render(request, 'registro.html', {"form": form, "contra": password}) 

@login_required(login_url='login')
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
            messages.error(request, "Email o contraseña invalidos")
    form=EmailAuthenticationForm()
    return render(request, "login.html", {"form": form}) 

@login_required(login_url='login')    
def cambiarContra(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user) # no cierra sesion
            user = CustomUser.objects.get(email = request.user)
            user.activo = True
            user.save()
            messages.success(request, 'Su contraseña se ha modificado con exito')
            return redirect("/")
    else:
        form = PasswordChangeForm(request.user)
    return render(request, "cambiarContra.html", {"form": form})

@login_required(login_url='login')
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
                messages.success(request, 'Su email se ha modificado con exito')
                return redirect('/')
            else:
                messages.error(request, "Ese email ya se encuentra registrado")
    return render(request, 'cambiarEmail.html', {"form": formulario})


@login_required(login_url='login')
def mi_perfil(request):
    usuario = request.user
    return render(request, "mi_perfil.html", {
        'usuario': usuario
    })
    

@login_required(login_url='login')
def mis_mascotas(request):
    mascotas = Perro.objects.filter(dueño=request.user)
    libretas_sanitarias = LibretaSanitaria.objects.filter(perro__in=mascotas)
    vacunas = Vacuna.objects.filter(libreta_sanitaria__in=libretas_sanitarias)
    return render(request, "mis_mascotas.html", {
        'mascotas': mascotas,
        'libretas_sanitarias': libretas_sanitarias,
        'vacunas': vacunas
    })

# Del veterinario:
@login_required(login_url='login')
@user_passes_test(is_superuser, login_url='home')
def lista_de_clientes(request):
    if (request.user.is_superuser == False):
        return redirect('home')
    queryset = CustomUser.objects.filter(is_superuser=False)
    nombre = request.GET.get('nombre')
    apellido = request.GET.get('apellido')
    dni = request.GET.get('dni')
    filtrado_por = ""
    if nombre:
        queryset = queryset.filter(nombre__icontains=nombre) 
        filtrado_por += "Nombre "
    if apellido:
        queryset = queryset.filter(apellido__icontains=apellido)
        filtrado_por += "Apellido "
    if dni:
        queryset = queryset.filter(dni__icontains=dni)
        filtrado_por += "DNI "
    form = FiltrosDeListadoDeClientes()
    context = {
        'clientes' : queryset,
        'form' : form,
        'filtrado' : filtrado_por
    }
    return render(request, "listado_de_clientes.html", context)

@login_required(login_url='login')
@user_passes_test(is_superuser, login_url='home')
def ver_perfil_cliente(request, dni):
    if (request.user.is_superuser == False):
            return redirect("home")

    cliente = CustomUser.objects.get(dni=dni)
    return render(request, "perfil_cliente.html", {"cliente": cliente})

@login_required(login_url='login')
@user_passes_test(is_superuser, login_url='home')
def ver_perros_cliente(request, dni):
    if (request.user.is_superuser == False):
        return redirect("home")

    cliente = CustomUser.objects.get(dni=dni)
    perros = Perro.objects.filter(dueño=cliente)
    libretas_sanitaras = LibretaSanitaria.objects.filter(perro__in=perros)
    vacunas = Vacuna.objects.filter(libreta_sanitaria__in=libretas_sanitaras)
    
    if request.method == "POST":
        perro_id = request.POST.get('mascota_id')
        if perros.filter(id=perro_id).exists():
            perro_a_borrar = Perro.objects.get(id=perro_id)
            perro_a_borrar.delete()
            redirect("perros_cliente", dni=dni)

    return render(request, "perros_cliente.html", {
        "cliente": cliente,
        "mascotas": perros,
        "libretas_sanitarias": libretas_sanitaras,
        "vacunas": vacunas,
    })

@login_required(login_url='login')
@user_passes_test(is_superuser, login_url='home')
def modificar_datos_cliente(request, dni_url):
    
    cliente = CustomUser.objects.get(dni = dni_url)
    if request.method == "POST":
        form = modificarDatosCliente(request.POST)
        if form.is_valid():
            nuevoNombre = request.POST.get('nombre')
            nuevoApellido = request.POST.get('apellido')
            nuevoDni = request.POST.get('dni')
            nuevoTelefono = request.POST.get('telefono')
            todosLosTfnos = CustomUser.objects.exclude(telefono=cliente.telefono).values_list('telefono', flat=True)
            todosLosDnis = CustomUser.objects.exclude(dni=cliente.dni).values_list('dni', flat=True)
            if nuevoDni in todosLosDnis:
                messages.error(request, "El dni ya se encuentra registrado")
                return render(request, "modificar_datos.html", {"form": form, "cliente": cliente})
            cliente.nombre = nuevoNombre
            cliente.apellido = nuevoApellido
            cliente.dni = nuevoDni
            cliente.telefono = nuevoTelefono
            cliente.save()
            messages.success(request, 'Datos modificados con exito')
            return redirect('perfil_cliente', cliente.dni)
    else:
        form = modificarDatosCliente()
    return render(request, "modificar_datos.html", {"form": form, "cliente": cliente})


@login_required(login_url='login')
@user_passes_test(is_superuser, login_url='home')
def modificar_datos_perro(request, dni, perro_id):
    perro = Perro.objects.get(id=perro_id)
    if request.method == "POST":
        form = ModificarDatosPerro(request.POST, perro=perro)
        
        if form.is_valid():
            perro.nombre = form.cleaned_data['nombre']
            perro.raza = form.cleaned_data['raza']
            perro.color = form.cleaned_data['color']
            perro.fecha_de_nacimiento = form.cleaned_data['fecha_de_nacimiento']
            perro.save()
            messages.success(request, 'Datos modificados con exito')
            return redirect('perros_cliente', dni)
    else:
        form = ModificarDatosPerro(perro=perro)
    return render(request, "modificar_datos_perro.html", {
        "form": form,
        "perro": perro
    })

def generar_pdf_perro(request, perro_id):
    perro = Perro.objects.get(id=perro_id)
    libreta_sanitaria = LibretaSanitaria.objects.get(perro=perro)
    vacunas = Vacuna.objects.filter(libreta_sanitaria=libreta_sanitaria)

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)

    generar_titulo(pdf)
    generar_logo(pdf)
    generar_datos_perro(pdf, perro)
    if vacunas:
        generar_tabla_vacunas(pdf, vacunas)

    else:
        generar_subtitulo_sin_vacunas(pdf)
    generar_fecha_generacion(pdf)

    pdf.showPage()
    pdf.save()

    name_file = f"libreta_sanitaria_{perro.nombre}.pdf"
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename={name_file}'

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    return response

def generar_titulo(pdf):
    titulo_x = A4[0] / 2
    titulo_y = A4[1] - 50

    pdf.setFont("Times-Bold", 16)
    pdf.drawCentredString(titulo_x, titulo_y, "Libreta Sanitaria.")
    pdf.setLineWidth(1)
    pdf.line(titulo_x - 70, titulo_y - 10, titulo_x + 70, titulo_y - 10)

def generar_logo(pdf):
    logo_width = 100
    logo_height = 100
    logo_x = 15
    logo_y = A4[1] - logo_height - 10

    pdf.drawImage("ohmydogApp/static/img/logo.png", logo_x, logo_y, width=logo_width, height=logo_height, mask="auto")

def generar_datos_perro(pdf, perro):
    pdf.setFont("Times-Roman", 12)

    datos_perro_x = 150
    datos_perro_y = A4[1] - 100

    datos_perro = [
        f"• Nombre: {perro.nombre}",
        f"• Raza: {perro.raza}",
        f"• Color: {perro.color}",
        f"• Sexo: {perro.sexo}",
        f"• Fecha de nacimiento: {perro.fecha_de_nacimiento}"
    ]

    for i, dato in enumerate(datos_perro):
        pdf.drawString(datos_perro_x, datos_perro_y - (i * 20), dato)

def generar_tabla_vacunas(pdf, vacunas):
    data = [["Vacuna", "Fecha de aplicación"]]
    for vacuna in vacunas:
        data.append([vacuna.tipo, vacuna.fecha.strftime("%d/%m/%Y")])

    # Calcular el ancho de cada columna de la tabla
    column_width = A4[0] - 2 * 150

    # Calcular la altura máxima disponible para la tabla
    tabla_max_height = A4[1] - 100 - (5 * 20) - 240

    # Crear la tabla
    table = Table(data, repeatRows=1)

    # Ajustar el estilo de la tabla
    table_style = TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.gray),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 12),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
        ("BACKGROUND", (0, 1), (-1, -1), colors.lightgrey),
        ("COLWIDTHS", (0, 0), (-1, -1), [column_width] * len(data[0])),
        ("TEXTCOLOR", (0, 0), (-1, -1), colors.black),
        ("LINEABOVE", (0, 0), (-1, -1), 1, colors.black),
        ("LINEBELOW", (0, 0), (-1, -1), 1, colors.black),
        ("LINEBEFORE", (0, 0), (-1, -1), 1, colors.black),
        ("LINEAFTER", (0, 0), (-1, -1), 1, colors.black),
        ("BOX", (0, 0), (-1, -1), 1, colors.black),
    ])

    # Configurar el estilo para que la tabla se extienda hacia abajo
    if len(table._argW) >= column_width:
        table_style.add("SPAN", (0, 0), (-1, 0))
        table_style.add("VALIGN", (0, 0), (-1, 0), "MIDDLE")

    table.setStyle(table_style)

    # Dibujar la tabla en el PDF
    table.wrapOn(pdf, 150, A4[1] - 210 - (len(data) * 20))
    table.drawOn(pdf, 150, A4[1] - 210 - (len(data) * 20))

def generar_subtitulo_sin_vacunas(pdf):
    pdf.setFont("Times-Bold", 14)
    pdf.drawString(230, A4[1] - 250, "No posee vacunas.")
    pdf.line(220, A4[1] - 260, 350, A4[1] - 260)

def generar_fecha_generacion(pdf):
    fecha_generacion = timezone.now().strftime("%d/%m/%Y %H:%M:%S")
    fecha_generacion_x = A4[0] - 150
    fecha_generacion_y = 40

    pdf.setFont("Times-Roman", 12)
    pdf.setFillColor(colors.gray)

    pdf.drawString(fecha_generacion_x, fecha_generacion_y, f"{fecha_generacion}")
