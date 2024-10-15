from django.shortcuts import render,redirect     # type: ignore
from django.contrib.auth.decorators import login_required   # type: ignore
from django.contrib.auth import logout as logout_django # type: ignore
from . import views

@login_required(login_url='/auth/login/')
def home(request):
    return render(request, 'home.html')

@login_required(login_url='/auth/login/')
def clientes(request):
    return render(request, 'clientes.html')

@login_required(login_url='/auth/login/')
def categorias(request):
    return render(request, 'categorias.html')

@login_required(login_url='/auth/login/')
def produtos(request):
    return render(request, 'produtos.html')

@login_required(login_url='/auth/login/')
def ordens(request):
    return render(request, 'ordens.html')

@login_required(login_url='/auth/login/')
def users(request):
    return render(request, 'users.html')

def logout_view(request):
    logout_django(request)
    return redirect('login')