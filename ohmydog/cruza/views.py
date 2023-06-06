from django.shortcuts import render
from .models import PerroCruza

# Create your views here.
def ver_perros_cruza(request):
    perros_cruza = PerroCruza.objects.all()
    return render(request, 'index_cruza.html', 
            {'perros_cruza': perros_cruza}
        )