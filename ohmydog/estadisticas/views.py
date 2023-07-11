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
    if perros: 
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
    if turnos:
        df_turnos = pd.DataFrame(list(turnos.values()))
        estadisticas_turnos = df_turnos.groupby('motivo').size().reset_index(name='cantidad')
        turnos = estadisticas_turnos['motivo']
        cant = estadisticas_turnos['cantidad']
        plt.pie(cant, labels=turnos, autopct='%1.1f%%')
        plt.axis('equal')
        plt.savefig('ohmydogApp/static/img/turnos.png', transparent=True)
        plt.close()
        estadisticas_dinamicas(request.GET.get('mes'))
    return render(request, 'estadisticas.html')


def estadisticas_dinamicas(mes):
    turnos = Turno.objects.filter(fecha__month=mes, fecha__year=2023)
    razas = turnos.values_list('perro__raza', flat=True)
    df_razas = pd.DataFrame({'raza': razas})
    estadisticas_razas = df_razas.groupby('raza').size().reset_index(name='cantidad')
    plt.bar(estadisticas_razas['raza'], estadisticas_razas['cantidad'])
    plt.xlabel('Raza')
    plt.ylabel('Cantidad de Turnos')
    plt.title(f'Estadísticas de Turnos - {mes}/{2023}')
    plt.xticks(rotation=45)
        # Verifica si el DataFrame está vacío
    if not estadisticas_razas.empty:
        # Establece los valores del eje y como números enteros
        plt.yticks(range(int(max(estadisticas_razas['cantidad'])) + 1))
    else:
        # Establece un valor predeterminado para el máximo del eje y
        plt.yticks([0])
    plt.tight_layout()  # Ajusta los márgenes del gráfico automáticamente
    img_path = 'ohmydogApp/static/img/dinamicas.png' 
    plt.savefig(img_path, transparent=True)
    plt.close()
    
