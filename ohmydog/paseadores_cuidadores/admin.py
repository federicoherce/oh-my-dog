from django.contrib import admin
from .models import PaseadorCuidador
# Register your models here.


class PaseadorCuidadorAdmin(admin.ModelAdmin):
    list_display=("nomyap", "email")
    
    
    
admin.site.register(PaseadorCuidador, PaseadorCuidadorAdmin)

