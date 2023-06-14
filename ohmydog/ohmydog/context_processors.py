from donaciones import models

def objeto_context(request):
    campana = models.Campaña.objects.first()
    return {'campana': campana}