from django.contrib import admin
from .models import Perdidos
# Register your models here.


class PerdidosAdmin(admin.ModelAdmin):
    list_display=("nombre", "estado")
    
    
    
admin.site.register(Perdidos, PerdidosAdmin)
