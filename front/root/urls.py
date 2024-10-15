from django.contrib import admin # type: ignore
from django.urls import path, include # type: ignore
from django.shortcuts import redirect # type: ignore


include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('usuarios.urls')),
    path('', include('dashboard.urls')),
    path('', lambda request: redirect('login', permanent=False)), 
]