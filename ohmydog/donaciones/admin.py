from django.contrib import admin
from .models import Campaña

# Register your models here.

class CampañaAdmin(admin.ModelAdmin):
    list_display=("nombre", "finalizada")

admin.site.register(Campaña, CampañaAdmin)