from django.contrib import admin
from .models import Perro

# Register your models here.

class PerrosAdmin(admin.ModelAdmin):
    list_display=("nombre", "sexo")


admin.site.register(Perro, PerrosAdmin)
