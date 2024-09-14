
from django.urls import path # type: ignore
from . import views

urlpatterns = [
 
    path('cadastro/', views.cadastro, name='cadastro'),
    path('login/', views.login, name='login'),
    path('plataforma/', views.plataforma, name='plataforma'),
]