from donaciones import models
import json

def objeto_context(request):
    campana = models.Campaña.objects.first()
    return {'campana': campana}

def redes(request):
    with open("ohmydog/ohmydogApp/redes.json") as redes:
        datos_redes = json.load(redes)
    redes_sociales = datos_redes['redes_sociales']
    formas_contacto = datos_redes['formas_contacto']
    
    facebook = redes_sociales[0]['enlace']
    twitter = redes_sociales[1]['enlace']
    instagram = redes_sociales[2]['enlace']
    mail = formas_contacto[0]['dato']
    telefono = formas_contacto[1]['dato']

    return {
        'facebook': facebook,
        'twitter': twitter,
        'instagram': instagram,
        'mail': mail,
        'telefono': telefono
    }