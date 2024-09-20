from django.shortcuts import render, HttpResponse, redirect  # type: ignore
from django.contrib.auth.models import User # type: ignore
from django.contrib.auth import authenticate, login as login_django, logout as logout_django # type: ignore
from django.contrib.auth import login as login_django   # type: ignore
from django.contrib.auth.decorators import login_required   # type: ignore
from . import views

def cadastro(request):
    if request.method == 'GET':
        return render(request, 'cadastro.html')
    else:
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = User.objects.filter(username=username).first()

        if user:
            return HttpResponse('Usuário já existe')
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
        return HttpResponse('Usuário cadastrado com sucesso')


def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            login_django(request, user)
            return redirect('home')  
        else:
            return HttpResponse('Usuário ou senha inválidos')

def logout_view(request):
    logout_django(request)
    return redirect('login')

