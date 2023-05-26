from django.contrib import admin
from .models import Turno

# Register your models here.

class TurnosAdmin(admin.ModelAdmin):
    list_display=("cliente", "cliente_asistio")


admin.site.register(Turno, TurnosAdmin)

