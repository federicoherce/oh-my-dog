# from django.views.generic import View
from .forms import CrearPago, TarjetaForm
from .models import Pago
from turnos.models import Turno
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse

# Create your views here.
@user_passes_test(lambda u: u.is_superuser) 
def pagar_con_tarjeta(request, monto):
    if request.method == 'POST':
        form = TarjetaForm(request.POST)
        if form.is_valid():
            numero_tarjeta = form.cleaned_data['numero_tarjeta']
            fecha_vencimiento = form.cleaned_data['fecha_vencimiento']
            nombre_titular = form.cleaned_data['nombre_titular']
            codigo_seguridad = form.cleaned_data['codigo_seguridad']
            # Resto de la lógica...
            messages.success(request, 'Pago exitoso!')
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
def pagar_turno(request):

    if request.method == 'POST':
        form = CrearPago(request.POST)
        if form.is_valid():
            Pago.objects.create(monto=request.POST['monto'])
            monto = request.POST.get('monto')
            metodo_pago = request.POST['metodo_pago']
            if metodo_pago == 'tarjeta':
                return redirect('pagos:pagar_con_tarjeta', monto=monto)
            elif metodo_pago == 'cripto':
                return redirect('pagos:escanear_qr', monto=monto)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
    else:
        form = CrearPago()
    return render(request, 'pagar_turno.html')

def escanear_qr(request, monto):
    if request.method == 'POST':
        opcion = request.POST.get('opcion')

        if opcion == 'pagado':
            # Procesar el pago exitoso y mostrar el mensaje
            messages.success(request, 'Pago exitoso!')
            return redirect('home')  # Redirigir al home
        else:
            return redirect('pagos:pagar_turno')  # Redirigir a la página pagar_turno


    context = {
        'monto': monto,
    }
   
    return render(request, 'escanear_qr.html', context)