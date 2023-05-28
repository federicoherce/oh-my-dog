# from django.views.generic import View
from .forms import CrearPago, CrearTarjeta
from .models import Pago, Tarjeta
from turnos.models import Turno
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse

# Create your views here.
@user_passes_test(lambda u: u.is_superuser) 
def pagarConTarjeta(request):
    if request.method == "POST":
        form = CrearTarjeta(request.POST)
        if form.is_valid():
            Tarjeta.objects.create(nombreTitular=request.POST['nombreTitular'], 
                                 fechaVencimiento=request.POST['fechaVencimiento'],
                                 numeroTarjeta=request.POST['numeroTarjeta'],
                                 codigoSeguridad=request.POST['codigoSeguridad'])
            return redirect('home')
    else:
        form = CrearTarjeta()
    return render(request, 'ventana_pago.html', {
        'form': form
    })

@user_passes_test(lambda u: u.is_superuser) 
def pagarTurno(request, turno_id):
    turno = Turno.objects.all(Turno, id=turno_id)

    if request.method == 'POST':
    
        monto = request.POST.get('monto')
        pago = Pago(turno=turno, monto=monto)
        pago.save()
        metodo_pago = request.POST['metodo_pago']
        if metodo_pago == 'tarjeta':
            return redirect('pagar_con_tarjeta', pago_id=pago.id)
        elif metodo_pago == 'cripto':
            return redirect('escanear_qr', pago_id=pago.id)

    return render(request, 'pagar_turno.html', {'turno': turno})