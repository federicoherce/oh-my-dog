# from django.views.generic import View
import decimal
from .forms import CrearPago, TarjetaForm
from .models import Pago
from autenticacion.models import CustomUser
from donaciones.models import Donacion, Campaña
from turnos.models import Turno
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse

# Create your views here.
def pagar_con_tarjeta(request, monto, dni):
    if monto == '0':
        messages.success(request, 'Su monto a favor por las donaciones realizadas cubre el total del turno!')
        return redirect('home')
    if request.method == 'POST':
        form = TarjetaForm(request.POST)
        if form.is_valid():
            numero_tarjeta = form.cleaned_data['numero_tarjeta']
            fecha_vencimiento = form.cleaned_data['fecha_vencimiento']
            nombre_titular = form.cleaned_data['nombre_titular']
            codigo_seguridad = form.cleaned_data['codigo_seguridad']
            # Resto de la lógica...
            user = CustomUser.objects.get(dni=dni)
            user.monto_a_favor = 0
            user.save()
            messages.success(request, 'Pago exitoso!')
            return redirect('home')
        else:
            # El formulario no es válido, mostrar mensajes de error
            for errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
    else:
        form = TarjetaForm()

    context = {
        'monto': monto,
        'form': form,
        'dni': dni
    }

    return render(request, 'pagar_con_tarjeta.html', context)

def pagar_donacion(request, monto, tipo, nombre, campana):
    if request.method == 'POST':
        form = TarjetaForm(request.POST)
        if form.is_valid():
            numero_tarjeta = form.cleaned_data['numero_tarjeta']
            fecha_vencimiento = form.cleaned_data['fecha_vencimiento']
            nombre_titular = form.cleaned_data['nombre_titular']
            codigo_seguridad = form.cleaned_data['codigo_seguridad']
            # Resto de la lógica...
            if request.user.is_authenticated:
                user = request.user
                user.monto_a_favor = user.monto_a_favor + decimal.Decimal(monto) * decimal.Decimal(0.20)
                user.save()
            if (tipo == "Campaña"): 
                cmp = Campaña.objects.get(id=campana)
                Donacion.objects.create(monto=monto, nombre=nombre, tipo=tipo, campana=cmp)
            else:
                Donacion.objects.create(monto=monto, nombre=nombre, tipo=tipo)
            messages.success(request, 'Donacion exitosa!')
            return redirect('home')
        else:
            # El formulario no es válido, mostrar mensajes de error
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
    else:
        form = TarjetaForm()

    context = {
        'monto': monto,
        'form': form,
    }

    return render(request, 'pagar_con_tarjeta.html', context)

@user_passes_test(lambda u: u.is_superuser) 
def pagar_turno(request, dni):

    if request.method == 'POST':
        form = CrearPago(request.POST)
        if form.is_valid():
            user = CustomUser.objects.get(dni=dni)
            Pago.objects.create(monto=request.POST['monto'])
            if decimal.Decimal(request.POST.get('monto')) - user.monto_a_favor > 0:
                monto = decimal.Decimal(request.POST.get('monto')) - user.monto_a_favor
            else:
                monto = 0
            metodo_pago = request.POST['metodo_pago']
            if metodo_pago == 'tarjeta':
                return redirect('pagos:pagar_con_tarjeta', monto=monto, dni=dni)
            elif metodo_pago == 'cripto':
                return redirect('pagos:escanear_qr', monto=monto, dni=dni)
        else:
            for errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
    else:
        form = CrearPago()
    return render(request, 'pagar_turno.html')

def escanear_qr(request, monto, dni):
    if monto == '0':
        user = CustomUser.objects.get(dni=dni)
        user.monto_a_favor = 0
        user.save()
        messages.success(request, 'Su monto a favor por las donaciones realizadas cubre el total del turno!')
        return redirect('home')
    if request.method == 'POST':
        opcion = request.POST.get('opcion')

        if opcion == 'pagado':
            user = CustomUser.objects.get(dni=dni)
            user.monto_a_favor = 0
            user.save()
            # Procesar el pago exitoso y mostrar el mensaje
            messages.success(request, 'Pago exitoso!')
            return redirect('home')  # Redirigir al home
        else:
            return redirect('pagos:pagar_turno', dni=dni)  # Redirigir a la página pagar_turno


    context = {
        'monto': monto,
        'dni': dni
    }
   
    return render(request, 'escanear_qr.html', context)