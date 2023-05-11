from django.shortcuts import render, HttpResponse



def home(request):
    return render(request, "home.html", {"user": request.user})

