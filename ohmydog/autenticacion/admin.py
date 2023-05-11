from django.contrib import admin
from autenticacion.models import CustomUser

# Register your models here.

class ClientesAdmin(admin.ModelAdmin):
    list_display=("email", "nombre", "apellido")
    search_fields=("nombre", "telefono")



admin.site.register(CustomUser, ClientesAdmin)
