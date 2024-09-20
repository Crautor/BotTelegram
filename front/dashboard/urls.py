
from django.urls import path # type: ignore
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('/clientes/', views.clientes, name='clientes'),
    path('/categorias/', views.categorias, name='categorias'),
    path('/produtos/', views.produtos, name='produtos'),
    path('/ordens/', views.ordens, name='ordens'),
    path('/users/', views.users, name='users'),
    path('logout/', views.logout_view, name='logout'),
]