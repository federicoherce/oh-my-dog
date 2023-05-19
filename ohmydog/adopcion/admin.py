from django.contrib import admin
from adopcion.models import Adopcion

# Register your models here.

class AdopcionAdmin(admin.ModelAdmin):
    list_display=("publicado_por", "nombre")

admin.site.register(Adopcion, AdopcionAdmin)