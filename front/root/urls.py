from django.contrib import admin # type: ignore
from django.urls import path, include # type: ignore


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('usuarios.urls')),
    # path('home/', home_view, name='home'),  
    # path('', include('root.urls')),        
]
