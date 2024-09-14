from django.shortcuts import render, HttpResponse # type: ignore
from django.contrib.auth.models import User # type: ignore
from django.contrib.auth import authenticate # type: ignore
from django.contrib.auth import login as login_django # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore

def cadastro(request):
    if request.method == 'GET':
        return render(request, 'cadastro.html')
    else:
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user= User.objects.filter(username=username).first()

        if user:
            return HttpResponse('Usuário já existe')
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
        return HttpResponse('usuario cadastrado com sucesso')
        

def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            login_django(request, user)
            return HttpResponse('Usuário logado com sucesso')
        else:
            return HttpResponse('Usuário ou senha inválidos')
        
@login_required(login_url='/auth/login/')
def plataforma(request):
    return HttpResponse('plataforma')