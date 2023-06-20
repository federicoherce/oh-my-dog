from django.shortcuts import redirect

def veterinario_restringido(view_func):
    def wrapper(request, *args, **kwargs):
        # Verificar si el usuario es un veterinario
        if request.user.is_superuser:
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper

def veterinario_required(view_func):
    def wrapper(request, *args, **kwargs):
        # Verificar si el usuario es un veterinario
        if request.user.is_superuser:
            # Permitir el acceso a la vista
            return view_func(request, *args, **kwargs)
        else:
            # Redirigir a una página de acceso denegado o mostrar un mensaje de error
            return redirect('home')
    return wrapper