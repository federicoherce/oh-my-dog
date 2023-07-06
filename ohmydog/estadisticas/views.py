from django.shortcuts import render, HttpResponse
import pandas as pd
from perros.models import Perro
from turnos.models import Turno
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('agg')

# Create your views here.


def ver_estadisticas(request):
    perros = Perro.objects.all()
    df_perros = pd.DataFrame(list(perros.values()))
    estadisticas_razas = df_perros.groupby('raza').size().reset_index(name='cantidad')
    razas = estadisticas_razas['raza']
    cantidades = estadisticas_razas['cantidad']
    # Crea el gráfico circular
    plt.pie(cantidades, labels=razas, autopct='%1.1f%%')
    plt.axis('equal')  # Para que el gráfico sea un círculo en lugar de una elipse
    # Guarda el gráfico como una imagen
    plt.savefig('ohmydogApp/static//img/razas.png', transparent=True)
    plt.close() 
    
    turnos = Turno.objects.all()
    df_turnos = pd.DataFrame(list(turnos.values()))
    estadisticas_turnos = df_turnos.groupby('motivo').size().reset_index(name='cantidad')
    turnos = estadisticas_turnos['motivo']
    cant = estadisticas_turnos['cantidad']
    plt.pie(cant, labels=turnos, autopct='%1.1f%%')
    plt.axis('equal')
    plt.savefig('ohmydogApp/static/img/turnos.png', transparent=True)
    plt.close()
    return render(request, 'estadisticas.html')
    
