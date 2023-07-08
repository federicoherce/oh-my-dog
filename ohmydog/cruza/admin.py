from django.contrib import admin
from .models import PerroCruza
# Register your models here.


class PerroCruzaAdmin(admin.ModelAdmin):
    list_display=("dueño", "perro")
    
    
    
admin.site.register(PerroCruza, PerroCruzaAdmin)

